import unittest
import os
import graphene
import collections

from sqlalchemy.orm import sessionmaker

from cc.models import engine, Base, Ouvrage, Category, OuvrageComponent
from cc.schema import schema

    
class TestSchemaQuery(unittest.TestCase):

    """Runs some graphql query against the schema to check this one is corectly
    configured."""

    def setUp(self):
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
        session = session()
        self.cat_1_1 = Category(owner_id=1, name='placo')
        self.cat_1_2 = Category(owner_id=1, name='placo_spe')
        self.cat_2 = Category(owner_id=2, name='beton')
        self.ouvrage_1_parent = Ouvrage(
                name='placo isole',
                owner_id=1,
                is_in_owner_library=True,
                category=self.cat_1_1,
                unit='m2')
        self.ouvrage_1_kid1 = Ouvrage(
                name='BA13',
                owner_id=1,
                is_in_owner_library=True,
                category=self.cat_1_1,
                unit='U')
        self.ouvrage_1_kid2 = Ouvrage(
                name='montant placo',
                owner_id=1,
                is_in_owner_library=True,
                category=self.cat_1_2,
                unit='ml')
        self.ouvrage_2 = Ouvrage(
                name='ciment',
                owner_id=2,
                is_in_owner_library=True,
                category=self.cat_2,
                unit='ml')
        session.add_all([self.cat_1_1, self.cat_1_2, self.cat_2, self.ouvrage_1_parent, self.ouvrage_1_kid1, self.ouvrage_1_kid2, self.ouvrage_2])
        session.commit()

    def tearDown(self):
        os.remove('database.sqlite3')

    def test_resolve_commands(self):
        # Arrange
        testcases = [
            # 1. CATEGORIES
            {
                "title": "'categories' should resolve all categories",
                "query": """
                    {
                      categories {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "categories": [
                        collections.OrderedDict({"id": "1", "name": "placo"}),
                        collections.OrderedDict({"id": "2", "name": "placo_spe"}),
                        collections.OrderedDict({"id": "3", "name": "beton"}),
                    ]
                }),
            },
            {
                "title": "categories(name=\"lac\") should resolve categories with \"pla\" in their name",
                "query": """
                    {
                      categories(name: "lac") {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "categories": [
                        collections.OrderedDict({"id": "1", "name": "placo"}),
                        collections.OrderedDict({"id": "2", "name": "placo_spe"}),
                    ]
                }),
            },
            # 2. OUVRAGES
            {
                "title": "'ouvrages' should resolve all ouvrages",
                "query": """
                    {
                      ouvrages {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "1", "name": "placo isole"}),
                        collections.OrderedDict({"id": "2", "name": "BA13"}),
                        collections.OrderedDict({"id": "3", "name": "montant placo"}),
                        collections.OrderedDict({"id": "4", "name": "ciment"}),
                    ]
                }),
            },
            {
                "title": "ouvrage(id: 2) should resolve the good one ouvrage",
                "query": """
                    {
                      ouvrage(id: 2) {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrage": collections.OrderedDict({"id": "2", "name": "BA13"}),
                }),
            },
            {
                "title": "ouvrage(id: [2, 3]) should resolve the good ouvrages",
                "query": """
                    {
                      ouvrages(ids: [2, 3]) {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "2", "name": "BA13"}),
                        collections.OrderedDict({"id": "3", "name": "montant placo"}),
                    ]
                }),
            },
            {
                "title": "ouvrages(category: 1) should resolve ouvrages of the category",
                "query": """
                    {
                      ouvrages(category: 1) {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "1", "name": "placo isole"}),
                        collections.OrderedDict({"id": "2", "name": "BA13"}),
                    ]
                }),
            },
            {
                "title": "ouvrages(categories: [1, 3]) should resolve ouvrages of the categories",
                "query": """
                    {
                      ouvrages(categories: [1, 3]) {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "1", "name": "placo isole"}),
                        collections.OrderedDict({"id": "2", "name": "BA13"}),
                        collections.OrderedDict({"id": "4", "name": "ciment"}),
                    ]
                }),
            },
            {
                "title": "ouvrages(ids: [1, 4], category: 1) should resolve ouvrages with both conditions",
                "query": """
                    {
                      ouvrages(ids: [1, 4], category: 1) {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "1", "name": "placo isole"}),
                    ]
                }),
            },
            {
                "title": "ouvrages(name: \"laco\") should resolve ouvrages with \"laco\" in their name",
                "query": """
                    {
                      ouvrages(name: "laco") {
                        id
                        name
                      }
                    }
                """,
                "expected": collections.OrderedDict({
                    "ouvrages": [
                        collections.OrderedDict({"id": "1", "name": "placo isole"}),
                        collections.OrderedDict({"id": "3", "name": "montant placo"}),
                    ]
                }),
            },
        ]

        # Act
        # Assert
        for test in testcases:
            result = schema.execute(test["query"])

            if result.errors:
                raise Exception(result.errors, test["title"])

            self.assertEqual(len(result.data), len(test["expected"]), test["title"])
            self.assertEqual(result.data, test["expected"], test["title"])

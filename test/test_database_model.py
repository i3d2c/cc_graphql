import unittest
import os

from sqlalchemy.orm import sessionmaker

from cc.models import engine, Base, Ouvrage, Category, OuvrageComponent


class TestDatabaseModel(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.session = session()

    def tearDown(self):
        os.remove('database.sqlite3')

    def test_ouvrage_should_contain_its_components(self):
        # 1. Create categories
        placo = Category(owner_id=12, name='placo')

        # 2. Create ouvrage and components
        ouvrage = Ouvrage(
                name='placo isole',
                owner_id=12,
                is_in_owner_library=True,
                category=placo,
                unit='m2')
        component1 = Ouvrage(
                name='BA13',
                owner_id=12,
                is_in_owner_library=True,
                category=placo,
                unit='U')
        component2 = Ouvrage(
                name='montant',
                owner_id=12,
                is_in_owner_library=True,
                category=placo,
                unit='ml')

        # 3. Link components to ouvrage
        oc1 = OuvrageComponent(
                ouvrage=ouvrage,
                component=component1,
                component_formula='ceil(L/1.20)',
                position=1)
        oc2 = OuvrageComponent(
                ouvrage=ouvrage,
                component=component2,
                component_formula='ceil(L/60)',
                position=2)

        self.session.add_all([placo, ouvrage, component1, component2, oc1, oc2])
        self.session.commit()

        resulting_ouvrage = self.session.query(Ouvrage).\
                filter(Ouvrage.name=="placo isole").\
                join(Ouvrage.components).all()[0]
        self.assertEqual(len(resulting_ouvrage.components), 2)
        self.assertEqual(resulting_ouvrage.components[0].component.name, 'BA13')
        self.assertEqual(resulting_ouvrage.components[1].component.name, 'montant')

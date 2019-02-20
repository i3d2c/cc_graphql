import unittest
import contextlib
import os

from cc.models import engine, db_session, Base, Ouvrage, Category, OuvrageComponent
from sqlalchemy import MetaData


class TestDatabase(unittest.TestCase):

    """Test case docstring."""

    def tearDown(self):
        os.remove('database.sqlite3')

    def test_creation(self):
        Base.metadata.create_all(bind=engine)

        # 1. Create categories
        placo = Category(owner_id=42, name='placo')
        beton = Category(owner_id=12, name="beton")
        db_session.add_all([placo, beton])
        db_session.commit()

        # 2. Create ouvrage and components
        ouvrage = Ouvrage(name='placo isole', owner_id=12, is_in_owner_library=True, category_id=placo.id, category=placo, unit='m2')
        component1 = Ouvrage(name='BA13', owner_id=12, is_in_owner_library=True, category_id=placo.id, category=placo, unit='U')
        component2 = Ouvrage(name='montant', owner_id=12, is_in_owner_library=True, category_id=placo.id, category=placo, unit='ml')
        db_session.add_all([ouvrage, component1, component2])
        db_session.commit()

        # 3. Link components to ouvrage
        oc1 = OuvrageComponent(component_id=component1.id, component_formula='ceil(L/1.20)', position=1)
        oc2 = OuvrageComponent(component_id=component2.id, component_formula='ceil(L/60)', position=2)
        ouvrage.components.append(oc1)
        ouvrage.components.append(oc2)

        resulting_ouvrage = Ouvrage.query.all()[0]
        self.assertEqual(len(resulting_ouvrage.components), 2)

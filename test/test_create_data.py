import unittest
import contextlib
import os

from cc.models import engine, Base, Ouvrage, Category, OuvrageComponent
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker


class TestDatabase(unittest.TestCase):

    """Test case docstring."""

    def tearDown(self):
        #os.remove('database.sqlite3')
        pass

    def test_creation(self):
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
        s = session()

        # 1. Create categories
        placo = Category(owner_id=12, name='placo')
        beton = Category(owner_id=42, name="beton")

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

        #s.add_all([placo, beton, ouvrage, component1, component2, oc1, oc2])
        #s.commit()
        
        s.add_all([ouvrage, component1, component2, oc1, oc2])
        s.commit()


        resulting_ouvrage = s.query(Ouvrage).\
                filter(Ouvrage.name=="placo isole").\
                join(Ouvrage.components).all()[0]
        self.assertEqual(len(resulting_ouvrage.components), 2)
        self.assertEqual(resulting_ouvrage.components[0].component.name, 'BA13')
        self.assertEqual(resulting_ouvrage.components[1].component.name, 'montant')

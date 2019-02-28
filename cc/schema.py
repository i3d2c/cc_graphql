import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from cc.models import db_session, Category as CategoryModel, Ouvrage as OuvrageModel, OuvrageComponent as OuvrageComponentModel


class Category(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel


class Ouvrage(SQLAlchemyObjectType):
    class Meta:
        model = OuvrageModel


class OuvrageComponent(SQLAlchemyObjectType):
    class Meta:
        model = OuvrageComponentModel

class Query(graphene.ObjectType):
    categories = graphene.List(Category)
    ouvrages = graphene.List(Ouvrage)
    ouvrage = graphene.Field(Ouvrage, id=graphene.Int())
    
    def resolve_categories(self, info):
        query = Category.get_query(info)
        return query.all()

    def resolve_ouvrage(self, info, id):
        query = Ouvrage.get_query(info)
        print(query)
        return query.get(id)

    def resolve_ouvrages(self, info):
        query = Ouvrage.get_query(info)
        return query.all()


schema = graphene.Schema(query=Query)

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Category as CategoryModel, Ouvrage as OuvrageModel


class Category(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel
        interfaces = (relay.Node, )


class CategoryConnection(relay.Connection):
    class Meta:
        node = Category


class Ouvrage(SQLAlchemyObjectType):
    class Meta:
        model = OuvrageModel
        interfaces = (relay.Node, )


class OuvrageConnection(relay.Connection):
    class Meta:
        node = Ouvrage


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_ouvrages = SQLAlchemyConnectionField(OuvrageConnection)
    all_categorys = SQLAlchemyConnectionField(CategoryConnection, sort=None)

schema = graphene.Schema(query=Query)

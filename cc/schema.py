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
    categories = graphene.List(Category, name=graphene.String())
    ouvrages = graphene.List(Ouvrage,
            ids=graphene.List(graphene.Int),
            category=graphene.Int(),
            categories=graphene.List(graphene.Int),
            name=graphene.String())
    ouvrage = graphene.Field(Ouvrage, id=graphene.Int())
    
    def resolve_categories(self, info, name=None):
        query = Category.get_query(info)
        if name is not None:
            query = query.filter(CategoryModel.name.like("%"+name+"%"))
        return query.all()

    def resolve_ouvrage(self, info, id):
        query = Ouvrage.get_query(info)
        return query.get(id)

    def resolve_ouvrages(self, info, ids=None, category=None, categories=None, name=None):
        query = Ouvrage.get_query(info)
        if ids is not None:
            query = query.filter(OuvrageModel.id.in_(ids))
        if category is not None:
            query = query.join(CategoryModel).filter(CategoryModel.id==category)
        if categories is not None:
            query = query.join(CategoryModel).filter(CategoryModel.id.in_(categories))
        if name is not None:
            query = query.filter(OuvrageModel.name.like("%"+name+"%"))
        return query.all()


schema = graphene.Schema(query=Query)

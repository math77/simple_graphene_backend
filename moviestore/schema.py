import graphene
import moviestore.movies.schema

class Query(moviestore.movies.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(moviestore.movies.schema.Mutation, graphene.ObjectType):

    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

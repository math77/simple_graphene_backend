import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from moviestore.movies.models import Actor, Movie, Review, Watched, User

# O DjangoObjectType converte automaticamente um modelo django em um ObjectType.

class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review


class WatchedType(DjangoObjectType):
    class Meta:
        model = Watched


# Cada campo da classe representa uma consulta do graphql
class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)
    reviews = graphene.List(ReviewType, idMovie=graphene.Int())
    watcheds = graphene.List(WatchedType, idUser=graphene.Int())

    #metodos de resolver. Conectam as querys do esquema ao banco de dados.

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)

        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)

        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_reviews(self, info, **kwargs):
        idMovie = kwargs.get('idMovie')
        return Review.objects.filter(movie__id=idMovie)

    def resolve_watcheds(self, info, **kwargs):
        idUser = kwargs.get('idUser')
        return Watched.objects.filter(user__id=idUser)


class WatchedInput(graphene.InputObjectType):
    id = graphene.ID()
    movie = graphene.ID()
    user = graphene.ID()
    vote = graphene.Int()


class ReviewInput(graphene.InputObjectType):
    id = graphene.ID()
    comment = graphene.String()
    movie = graphene.ID()
    user = graphene.ID()


class CreateWatched(graphene.Mutation):
    # input de dados para o mutador
    class Arguments:
        input = WatchedInput(required=True)

    # resposta do payload
    ok = graphene.Boolean()
    watched = graphene.Field(WatchedType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        movie = Movie.objects.get(input.movie)
        user = User.objects.get(input.user)
        watched_instance = Watched(movie=movie, user=user, vote=input.vote)
        watched_instance.save()
        return CreateWatched(ok=ok, watched=watched_instance)


class CreateReview(graphene.Mutation):
    class Arguments:
        input = ReviewInput(required=True)

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        movie = Movie.objects.get(pk=input.movie)
        user = User.objects.get(pk=input.user)
        review_instance = Review(comment=input.comment, user=user, movie=movie)
        review_instance.save()
        return CreateReview(ok=ok, review=review_instance)


class Mutation(graphene.ObjectType):
    create_watched = CreateWatched.Field()
    create_review = CreateReview.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

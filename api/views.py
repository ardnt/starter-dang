import logging
import traceback

from graphene_django.views import GraphQLView

from .exceptions import NotLoggedException


logger = logging.getLogger('api.views.graphql')


class APIView(GraphQLView):
    """Override graphene_django.views.GraphQLView to turn on Graphiq in views
    instead of in urls
    """

    def __init__(self, *args, **kwargs):
        kwargs['graphiql'] = True
        return super().__init__(*args, **kwargs)

    def execute_graphql_request(self, *args, **kwargs):
        result = super().execute_graphql_request(*args, **kwargs)

        if hasattr(result, 'errors'):
            for error in result.errors or []:
                try:
                    e = error.original_error
                    if not isinstance(e, NotLoggedException):
                        msg = ''.join(
                            traceback.format_exception(type(e), e, e.__traceback__)
                        )
                        logger.error(msg)
                except AttributeError:
                    logger.error(error)

        return result

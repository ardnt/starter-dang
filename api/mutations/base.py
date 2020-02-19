import graphene

from ..exceptions import NotLoggedException


class FormMutation(graphene.Mutation):
    """Abstract mutation class to dry out mutations that work with Django forms
    """

    class Meta:
        abstract = True

    @classmethod
    def mutate(cls, root, info, **arguments):
        form_data = cls.transform_arguments(info, arguments)
        form = cls.get_form(info, form_data)

        if form.is_valid():
            return cls.form_is_valid(info, form)

        error_messages = []
        for field, messages in form.errors.items():
            error_messages.extend(messages)
        raise NotLoggedException('; '.join(error_messages))

    @classmethod
    def form_is_valid(cls, info, form):
        raise NotImplementedError

    @classmethod
    def get_form(cls, info, form_data):
        raise NotImplementedError

    @classmethod
    def transform_arguments(cls, info, arguments):
        return arguments.get('input')

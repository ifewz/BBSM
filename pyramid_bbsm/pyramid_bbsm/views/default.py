from pyramid.view import view_config

from ..models import MyModel


@view_config(context=MyModel, renderer='pyramid_bbsm:templates/mytemplate.pt')
def my_view(request):
    return {'project': 'Pyramid_bbsm'}

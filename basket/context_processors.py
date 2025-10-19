from django.contrib.sessions.backends.db import SessionStore

from .basket import Basket


def basket(request):
    if not hasattr(request, 'session'):
        request.session = SessionStore()
    return {'basket': Basket(request)}
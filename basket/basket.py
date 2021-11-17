


class Basket():
    """
    A base Basket class, providing some default behaviours that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {'number': 12132311231}
        self.basket = basket

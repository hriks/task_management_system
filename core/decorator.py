from django.shortcuts import redirect


def auth_required(f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if 'authToken' in request.session.keys():
            from core.models import Operator
            operator = Operator.getAuthenticatedOperator(request)
            if operator:
                return f(request, operator, *args, **kwargs)
        return redirect('/')
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

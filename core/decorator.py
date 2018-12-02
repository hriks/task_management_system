from django.shortcuts import redirect


def auth_required(methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(view):
        def wrapper(request, *args, **kw):
            if 'authToken' in request.session.keys():
                from core.models import Operator
                operator = Operator.getAuthenticatedOperator(request)
                if operator:
                    return view(request, operator, *args, **kw)
            from django.contrib import messages
            messages.error(request, "Hi, You need to login to view this page.")
            return redirect('/')
        return wrapper

    return wrap

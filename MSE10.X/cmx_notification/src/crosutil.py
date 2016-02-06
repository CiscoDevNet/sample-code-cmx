
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

# here is the code for allowing other clients cross domain to access the resource from this site,
# if you want to get more detail about the cross domain access, please visit the :https://en.wikipedia.org/wiki/Cross-origin_resource_sharing

# methods: Optionally a list of methods that are allowed for this view. If not provided it will allow all methods that are implemented.
# headers: Optionally a list of headers that are allowed for this request.
# origin: '*' to allow all origins, otherwise a string with a URL or a list of URLs that might access the resource.
# max_age: The number of seconds as integer or timedelta object for which the preflighted request is valid.
# attach_to_all: True if the decorator should add the access control headers to all HTTP methods or False if it should only add them to OPTIONS responses.
# automatic_options: If enabled the decorator will use the default Flask OPTIONS response and attach the headers there, otherwise the view function will be called to generate an appropriate response.

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    # join the parameters with comma

    # get the value of http header 'Access-Control-Allow-Methods'
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))

    # get the value of http header 'Access-Control-Allow-Headers'
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)

    # get the value of http header 'Access-Control-Allow-Origin'
    if not isinstance(origin, str):
        origin = ', '.join(origin)

    # get the value of http header 'Access-Control-Max-Age'
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        # if not provided, make the default response options, which will allow all methods that are implemented.
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            # if enabled the decorator will use the default Flask OPTIONS response and attach the headers there,
            # otherwise the view function will be called to generate an appropriate response.
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
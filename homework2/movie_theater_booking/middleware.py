class ProxyPrefixMiddleware:
    """
    Ensures Django builds correct redirect URLs when the site is served behind
    a path-prefix reverse proxy like /proxy/8000.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = "/proxy/8000"

        # If SCRIPT_NAME already set, don't double-prefix anything.
        if not request.META.get("SCRIPT_NAME"):
            request.META["SCRIPT_NAME"] = prefix

        return self.get_response(request)
import logging

logger = logging.getLogger(__name__)

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_request(self, request):
        logger.info(f"Request: {request.method} {request.get_full_path()} from {request.META.get('REMOTE_ADDR')}")
        logger.debug(f"Headers: {request.headers}")
        if request.body:
            logger.debug(f"Body: {request.body}")

    def process_response(self, request, response):
        logger.info(f"Response status code: {response.status_code} for {request.method} {request.get_full_path()}")
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception: {exception}, Request: {request.method} {request.get_full_path()}")
        return None
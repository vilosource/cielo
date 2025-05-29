import logging

logger = logging.getLogger(__name__)


class DebugLoggingMiddleware:
    """Middleware to log request/response details for debugging authentication issues."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        logger.debug(f"=== REQUEST START ===")
        logger.debug(f"Method: {request.method}")
        logger.debug(f"Path: {request.path}")
        logger.debug(f"User: {request.user}")
        logger.debug(f"User authenticated: {getattr(request.user, 'is_authenticated', False)}")
        logger.debug(f"Session key: {request.session.session_key}")
        logger.debug(f"Session data: {dict(request.session)}")
        
        if hasattr(request, 'POST') and request.POST:
            logger.debug(f"POST data: {dict(request.POST)}")
        
        # Get response
        response = self.get_response(request)
        
        # Log response details
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"User after request: {request.user}")
        logger.debug(f"User authenticated after: {getattr(request.user, 'is_authenticated', False)}")
        logger.debug(f"Session key after: {request.session.session_key}")
        logger.debug(f"Session data after: {dict(request.session)}")
        logger.debug(f"=== REQUEST END ===")
        
        return response

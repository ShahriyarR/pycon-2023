from esmerald import EsmeraldInterceptor
from esmerald.requests import Request
from loguru import logger
from starlette.types import Receive, Scope, Send


class LoggingInterceptor(EsmeraldInterceptor):
    async def intercept(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        """
        Intercepts the messages being sent to the API before reaching
        out the API itself.
        """
        request = Request(scope=scope, receive=receive, send=send)
        method = request.method
        url = request.url
        logger.success(f"Method: {method}. URL: {url}. Logging into sentry...")

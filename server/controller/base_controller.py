import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.controller.controller import Controller
from utility.utility import ExceptionRequest
from fastapi import Request


def base_controller(app):
    c = Controller(app)
    router = c.includeRouter()
    
    @app.exception_handler(ExceptionRequest)
    async def global_exception_handler(request: Request, exc: ExceptionRequest):
        if isinstance(exc, ExceptionRequest):
            return c.setResponse(
                msg=exc.message,
                status_code=exc.status_code
            )
        return c.setResponse(
            msg="errore generico",
            status_code=500
        )   


    @router.get("/health")
    def health():
        return c.setResponse("Health check", {"status": "ok"})
    
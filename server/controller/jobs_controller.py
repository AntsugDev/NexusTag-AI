import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException, Request, File, Form, UploadFile, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response
from server.auth import verify_token
import shutil

def jobs_controller(admin_router):

    @admin_router.get("/job_failed/{document_id}/error", tags=["jobs"])
    def get_document_error(document_id: int, user: dict = Depends(verify_token)):
        if user.get("username") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden: Admin only")
        try:
            from database.model.jobs_failed import JobsFailed
            job_failed = JobsFailed()
            error_msg = job_failed.get_last_error(document_id)
            return response(msg="Error details retrieved", data={"error": error_msg})
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)
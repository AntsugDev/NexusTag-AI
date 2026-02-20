import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException, Request, Depends
from utility.utility import ExceptionRequest, response
from server.auth import verify_token

def jobs_controller(admin_router):

    @admin_router.get("/failed", tags=["jobs"])
    def get_all_jobs_failed(page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
        if user.get("username") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden: Admin only")
        try:
            from database.model.jobs_failed import JobsFailed
            job_failed = JobsFailed()
            
            items = job_failed.paginate(page=page, limit=limit)
            total = job_failed.count()
            
            # Formatta i metadati se presenti
            import json
            items_list = []
            for item in items:
                d = dict(item)
                if d.get("meta_data") and isinstance(d["meta_data"], str):
                    try:
                        d["meta_data"] = json.loads(d["meta_data"])
                    except:
                        pass
                items_list.append(d)

            return response(msg="Failed jobs list retrieved", data={
                "items": items_list,
                "total": total,
                "page": page,
                "limit": limit
            })
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)

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

    @admin_router.get("/status", tags=["jobs"])
    def get_scheduler_status(user: dict = Depends(verify_token)):
        if user.get("username") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden: Admin only")
        try:
            from scheduler.status import scheduler_status
            return response(msg="Scheduler status retrieved", data=scheduler_status.get_status())
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)

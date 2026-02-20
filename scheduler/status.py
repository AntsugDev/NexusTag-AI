import datetime

class SchedulerStatus:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SchedulerStatus, cls).__new__(cls)
            cls._instance.is_running = False
            cls._instance.last_run_start = None
            cls._instance.last_run_end = None
            cls._instance.job_id = "documents_jobs"
            cls._instance._scheduler = None
        return cls._instance

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def set_running(self, running: bool):
        self.is_running = running
        if running:
            self.last_run_start = datetime.datetime.now()
        else:
            self.last_run_end = datetime.datetime.now()

    def get_status(self):
        now = datetime.datetime.now()
        next_run = None
        
        if self._scheduler:
            job = self._scheduler.get_job(self.job_id)
            if job:
                next_run = job.next_run_time

        seconds_to_next = None
        if next_run:
            # next_run is offset-aware (UTC), now is naive. 
            # Need to handle timezone if next_run is aware.
            # Usually APScheduler uses aware datetimes if configured.
            if next_run.tzinfo:
                now_aware = datetime.datetime.now(next_run.tzinfo)
                seconds_to_next = max(0, (next_run - now_aware).total_seconds())
            else:
                seconds_to_next = max(0, (next_run - now).total_seconds())
            
        return {
            "is_running": self.is_running,
            "last_run_start": self.last_run_start.isoformat() if self.last_run_start else None,
            "last_run_end": self.last_run_end.isoformat() if self.last_run_end else None,
            "next_run": next_run.isoformat() if next_run else None,
            "seconds_to_next": int(seconds_to_next) if seconds_to_next is not None else None
        }

scheduler_status = SchedulerStatus()


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apscheduler.schedulers.background import BackgroundScheduler
from abc import ABC, abstractmethod

class Scheduler(ABC):
    def __init__(self, tag, trigger="cron", **kwargs):
        self.tag = tag
        self.trigger = trigger
        self.kwargs = kwargs

    @abstractmethod
    def handle(self):
        pass

    def register(self, scheduler):
        try:
            scheduler.add_job(
                self.handle, 
                trigger=self.trigger,
                id=self.tag,
                replace_existing=True,
                **self.kwargs
            )
            print(f"Job registered: {self.tag} with trigger {self.trigger} ({self.kwargs})")
        except Exception as e:
            raise e

    def failed(self, data):
        try:
            from database.model.jobs_failed import JobsFailed
            failed = JobsFailed()
            failed.insert(data)
        except Exception as e:
            raise e    

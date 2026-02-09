from scheduler.documents_jobs import DocumentsJobs

# Lista delle istanze dei job da registrare
jobs = [
    DocumentsJobs(),
    # Aggiungi qui altri job in futuro
]

def register_all_jobs(scheduler):
    for job in jobs:
        job.register(scheduler)

if __name__ == "__main__":
    import time
    from apscheduler.schedulers.background import BackgroundScheduler
    
    scheduler = BackgroundScheduler()
    register_all_jobs(scheduler)
    scheduler.start()
    
    print("Scheduler is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
    
from threading import Thread
from time import sleep, time
from plyer import notification

class CheckTimingThreading(Thread):
    def __init__(self, query, db, app) -> None:
        super().__init__(daemon=True)
        self.query = query
        self.db = db
        self.app = app

    def run(self):
        with self.app.app_context():
            while True:
                sleep(10)
                now = int(time())
                timings = self.query.query.all()
                for timing in timings:
                    if now >= timing.timestamp:
                        notes_content = timing.notes.content
                        self.db.session.delete(self.query.query.get(timing.id))
                        notification.notify(title="定时提醒",
			    		                    message=notes_content,
			    		                    app_icon="static/images/notes.ico",
			    		                    timeout=10
			    		)
                        self.db.session.commit()


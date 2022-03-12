from threading import Thread
from time import sleep, time
from plyer import notification

class CheckTimingThreading(Thread):
    def __init__(self, db_query) -> None:
        super().__init__(daemon=True)
        self.db_query = db_query

    def run(self):
        while True:
            sleep(10)
            now = int(time())
            timings = self.db_query.select("id, timestamp, notes_id", "timings")
            for timing in timings:
                if now >= timing[1]:
                    self.db_query.delete("timings", "id={}".format(timing[0]))
                    notes_content = self.db_query.select("id, content", "notes", "id={}".format(timing[2]))
                    notes_content = list(notes_content)[0][1]
                    notification.notify(title="定时提醒",
					                    message=notes_content,
					                    app_icon="static/images/notes.ico",
					                    timeout=10
					)


import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import static_graphic as vizual


class TestEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            vizual.viz()

if __name__ == "__main__":

    event_handler = TestEventHandler()
    observer = Observer()
    observer.schedule(event_handler,
                      path=vizual.WATCH_DIR,
                      recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

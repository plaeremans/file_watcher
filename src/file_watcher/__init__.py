import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


def execute_cmd(cmd_to_execute):
    subprocess.run(cmd_to_execute, shell=True)


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, cmd_to_execute):
        self.cmd_to_execute = cmd_to_execute

    def on_modified(self, event):
        if not event.is_directory:
            execute_cmd(self.cmd_to_execute)


def watch_for_changes(directory, cmd_to_execute):
    event_handler = FileChangeHandler(cmd_to_execute)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python file_watcher.py <directory_to_watch> <cmd to execute>")
        return 1

    directory_to_watch = sys.argv[1]
    cmd_to_execute = sys.argv[2:]
    print(str(cmd_to_execute))
    watch_for_changes(directory_to_watch, cmd_to_execute)

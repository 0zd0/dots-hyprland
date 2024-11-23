import hashlib
import logging
import shutil
import threading
import time
from pathlib import Path
from typing import List
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer
from config import config, SyncPair
from queue import Queue, Empty


class FolderHandler(FileSystemEventHandler):
    def __init__(self,
                 sync_pair: SyncPair,
                 source_to_target: bool
                 ):
        self.sync_pair = sync_pair
        self.source_to_target = source_to_target
        self.queue: Queue = Queue()

        self.source = sync_pair.source if source_to_target else sync_pair.target
        self.target = sync_pair.target if source_to_target else sync_pair.source

        self.logger = logging.getLogger(f"sync:"
                                        f"{sync_pair.source.name}"
                                        f"{'->' if source_to_target else '<-'}"
                                        f"{sync_pair.target.name}")

    def on_created(self, event: FileSystemEvent) -> None:
        if Path(event.src_path).is_relative_to(self.source):
            self.queue.put(("create", Path(event.src_path)))

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory and Path(event.src_path).is_relative_to(self.source):
            self.queue.put(("modify", Path(event.src_path)))

    def on_deleted(self, event: FileSystemEvent) -> None:
        if Path(event.src_path).is_relative_to(self.source):
            self.queue.put(("delete", Path(event.src_path)))

    def should_skip(self, path: str) -> bool:
        return any(x in path for x in self.sync_pair.excludes)

    def get_file_hash(self, path: Path) -> str:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def process_events(self) -> None:
        while True:
            try:
                event_type, src_path = self.queue.get(timeout=1.0)
                if self.should_skip(str(src_path)):
                    continue

                # Получаем относительный путь
                rel_path = src_path.relative_to(self.source)
                target_path = self.target / rel_path

                if event_type in ("create", "modify"):
                    if not src_path.exists():
                        continue

                    if src_path.is_file():
                        if (not target_path.exists() or
                                self.get_file_hash(src_path) != self.get_file_hash(target_path)):
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src_path, target_path)
                            self.logger.info(f"Synced: {rel_path}")
                    else:
                        target_path.mkdir(parents=True, exist_ok=True)

                elif event_type == "delete":
                    if target_path.exists():
                        if target_path.is_file():
                            target_path.unlink()
                        else:
                            shutil.rmtree(target_path)
                        self.logger.info(f"Deleted: {rel_path}")

            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error processing: {e}")


def start_sync(sync_pairs: List[SyncPair]):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S'
    )

    observers = []

    for pair in sync_pairs:
        handler1 = FolderHandler(pair, source_to_target=True)
        observer1 = Observer()
        observer1.schedule(handler1, str(pair.source), recursive=True)
        thread1 = threading.Thread(target=handler1.process_events, daemon=True)

        handler2 = FolderHandler(pair, source_to_target=False)
        observer2 = Observer()
        observer2.schedule(handler2, str(pair.target), recursive=True)
        thread2 = threading.Thread(target=handler2.process_events, daemon=True)

        observer1.start()
        observer2.start()
        thread1.start()
        thread2.start()

        observers.extend([observer1, observer2])

        logging.info(f"Started sync: {pair.source} <-> {pair.target}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        logging.info("Sync stopped")


if __name__ == '__main__':
    start_sync(config)

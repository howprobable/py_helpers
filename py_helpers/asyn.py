
from typing import Callable, Generic, TypeVar, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import traceback
import time
import threading

# Create a global ThreadPoolExecutor
_executor = ThreadPoolExecutor(max_workers=100)  # Adjust max_workers as needed
_futures = []


def parallel(task, *args, **kwargs):
    # Submit tasks to the global _executor
    future = _executor.submit(task, *args, **kwargs)
    _futures.append(future)
    return future

def wait_for_tasks(tasks: list[Future], verbose: bool = False): 
    if verbose: print(f"[Async] Waiting for {len(tasks)} tasks")
    for future in as_completed(tasks):
        if future.exception():
            exc = future.exception()
            if verbose: print(f"[Async] Task raised an exception: {exc}")
            traceback.print_exception(type(exc), exc, exc.__traceback__)

    time.sleep(0.3)
    if verbose: print(f"[Async] All tasks finished")

def wait_for_all_tasks(verbose: bool = False):
    if verbose: print(f"[Async] Waiting for all _futures: {len(_futures)}")
    for future in as_completed(_futures):
        if future.exception():
            exc = future.exception()
            if verbose: print(f"[Async] Task raised an exception: {exc}")
            traceback.print_exception(type(exc), exc, exc.__traceback__)

    time.sleep(0.3)
    if verbose: print(f"[Async] All _futures finished")



T = TypeVar("T")
class lockedObject(Generic[T]):
    def __init__(self, object: T):
        self._object: T = object
        self._lock = threading.Lock()

    def do(self, func: Callable[[T], Any]):
        ret = None

        with self._lock:
            ret = func(self._object)

            return ret

    def set(self, val: T):
        with self._lock:
            self._object = val

    def get(
        self,
    ) -> T:
        with self._lock:
            return self._object

    def copy(
        self,
    ) -> T:
        with self._lock:
            return self._object.copy()
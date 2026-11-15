import time


def with_retries(call, attempts=3, delay=0.5):
    """Call `call()` up to `attempts` times, waiting `delay` seconds between tries."""
    for attempt in range(1, attempts):
        try:
            return call()
        except ConnectionError:
            time.sleep(delay * attempt)
    raise RuntimeError(f"gave up after {attempts} attempts")

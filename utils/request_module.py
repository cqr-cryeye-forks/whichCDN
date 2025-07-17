import signal
import requests

class TimeoutException(Exception):
    pass

def requestTimeout(signum, frame):
    raise TimeoutException()

def do(hostname: str):
    try:
        return requests.get(hostname, timeout=10)
    except TimeoutException:
        print("\033[1;31m[!] Request timeout: test aborted\n\033[1;m")
        return None
    except requests.ConnectionError:
        print("\033[1;31m[!] Server not found: test aborted\n\033[1;m")
        return None
    finally:
        signal.alarm(0)

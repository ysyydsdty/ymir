""" for test """
import sys
from typing import Dict
import socketio


def update_taskstate(*args: tuple, **kwargs: Dict) -> None:
    print(f"update_taskstate: {args}, {kwargs}")


def main() -> int:
    url = sys.argv[1]
    namespace = sys.argv[2]

    print(f"connecting to url: {url}, namespace: {namespace}")

    sio = socketio.Client(logger=True)
    sio.connect(url, namespaces=[namespace], socketio_path='/ws/socket.io')
    sio.event(namespace=namespace)(update_taskstate)
    sio.wait()

    return 0


if __name__ == '__main__':
    # usage: python sio_client.py <url with http> <namespace begin with slash>
    sys.exit(main())

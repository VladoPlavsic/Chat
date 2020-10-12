from sender import Sender
from receiver import Receiver
import logging
import os
import sys


def main(message):
    HOST = 'localhost'
    QUEUE = 'hello'

    sender = Sender(HOST, QUEUE)

    sender._send(message)
    sender._close_connection()


if __name__ == "__main__":
    try:
        while(1):
            main(input())
    except KeyboardInterrupt:
        logging.warning('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

import pika
import logging
import os
import sys


class Sender:

    def __init__(self, host, exchange_name, routing_key):
        self._HOST = host
        self._EXCHANGE_NAME = exchange_name
        self._ROUTING_KEY = routing_key
        self._EXCHANGE_TYPE = 'topic'

        self._CONNECTION = self._connect()
        self._CHANNEL = self._CONNECTION.channel()

        self._create_exchange()

    def _connect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self._HOST))

    def _create_exchange(self):
        self._CHANNEL.exchange_declare(
            exchange=self._EXCHANGE_NAME, exchange_type=self._EXCHANGE_TYPE)

    def _send(self, message):
        self._CHANNEL.basic_publish(exchange=self._EXCHANGE_NAME,
                                    routing_key=self._ROUTING_KEY,
                                    body=message)

        print(f" [x] Sent {message}")

    def _close_connection(self):
        self._CONNECTION.close()


def main(message, routing_key, exchange):
    HOST = 'localhost'
    EXCHANGE = exchange
    sender = Sender(HOST, EXCHANGE, routing_key.strip())
    sender._send(f"{exchange}: {message}")
    sender._close_connection()


if __name__ == "__main__":
    try:
        while(1):
            data = input().split(' ')
            main((' ').join(data[1:]), data[0], sys.argv[1])
    except KeyboardInterrupt:
        logging.warning('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

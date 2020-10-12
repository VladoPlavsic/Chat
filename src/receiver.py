import pika
import logging
import sys
import os


class Receiver:

    def __init__(self, host, exchange_name, routing_key, callback):
        self._HOST = host
        self._EXCHANGE_NAME = exchange_name
        self._ROUTING_KEY = routing_key
        self._EXCHANGE_TYPE = 'topic'

        self.callback = callback

        self._CONNECTION = self._connect()
        self._CHANNEL = self._CONNECTION.channel()
        self._create_exchange()

        self._QUEUE_NAME = self._queueu_declare().method.queue

        self._bind_queue()
        self._start_consuming()

    def _connect(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self._HOST))

    def _queueu_declare(self):
        return self._CHANNEL.queue_declare(queue='', exclusive=True)

    def _create_exchange(self):
        for exchange in self._EXCHANGE_NAME:
            self._CHANNEL.exchange_declare(
                exchange=exchange, exchange_type=self._EXCHANGE_TYPE)

    def _bind_queue(self):
        for exchange in self._EXCHANGE_NAME:
            self._CHANNEL.queue_bind(
                exchange=exchange, queue=self._QUEUE_NAME, routing_key=self._ROUTING_KEY)

    def _start_consuming(self):
        self._CHANNEL.basic_consume(
            queue=self._QUEUE_NAME, on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._CHANNEL.start_consuming()


def callback(ch, method, properties, body):
    print(f" [X] Received {body.decode()}")


def main(bind_queue):
    HOST = 'localhost'
    EXCHANGE = bind_queue[2:]
    reciver = Receiver(HOST, EXCHANGE, bind_queue[1], callback)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

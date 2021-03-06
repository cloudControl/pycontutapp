from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from pollsys import settings
import pika
import urlparse
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Successfully provide')

        url_str = str(settings.amqpcreds['CLOUDAMQP_URL'])
        url = urlparse.urlparse(url_str)
        params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:], credentials=pika.PlainCredentials(url.username, url.password))

        connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='mailing')  # Declare a queue

        # create a function which is called on incoming messages
        def callback(ch, method, properties, body):
            print " [x] Received %r %s" % (json.loads(body), type(body))
            contents = json.loads(body)
            send_mail('Poll Expired', 'Poll {0} created by {1} is Expired.'.format(contents['message'], contents['created_by']), 'info@pollsys.de', [contents['email']], fail_silently=False)

        # set up subscription on the queue
        channel.basic_consume(callback,
            queue='mailing',
            no_ack=True)

        channel.start_consuming()  # start consuming (blocks)

        connection.close()

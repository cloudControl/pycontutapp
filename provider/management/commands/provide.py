from django.core.management.base import BaseCommand
import pika, urlparse
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Successfully provide')

        # Parse CLODUAMQP_URL (fallback to localhost)
        url_str = 'amqp://depbjmvqbpc_cloudcontrolled.com:BhLrII7ZcUQirRfANnYIWhyaSp85rQUx@bunny.cloudamqp.com/depbjmvqbpc_cloudcontrolled.com'
        url = urlparse.urlparse(url_str)
        params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:], credentials=pika.PlainCredentials(url.username, url.password))

        connection = pika.BlockingConnection(params) # Connect to CloudAMQP
        channel = connection.channel() # start a channel
        channel.queue_declare(queue='hello') # Declare a queue
        # send a message
        message = {'email':'fk@cloudcontrol.de', 'subject':'Hallo Felix', 'message':'Das ist eine email'}
        channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(message))
        print " [x] Sent 'Hello World!'"

        connection.close()
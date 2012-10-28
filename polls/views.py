from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll
from pollsys import settings
import pika
import urlparse
import json


def index(request):
    latest_poll_list = [p for p in Poll.objects.all().order_by('-pub_date') if not p.is_expired()]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                               context_instance=RequestContext(request))


def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))


def maintain(request):

    print('checking for ended Polls')
    # Parse CLODUAMQP_URL (fallback to localhost)
    url_str = str(settings.amqpcreds['CLOUDAMQP_URL'])
    print url_str
    url = urlparse.urlparse(url_str)
    params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:], credentials=pika.PlainCredentials(url.username, url.password))

    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='hello')  # Declare a queue

    expired_polls = [p for p in Poll.objects.all() if p.is_expired() and not p.finished]
    for poll in expired_polls:
        poll.finished = True
        poll.save()
        print('Poll {0} created by {1} with E-Mail {2} is Expired.'.format(poll.question, poll.created_by.username, poll.created_by.email))
        message = {'email': poll.created_by.email, 'created_by': poll.created_by.username, 'message': poll.question}
        channel.basic_publish(exchange='', routing_key='mailing', body=json.dumps(message))

    connection.close()

    return render_to_response('polls/index.html', {'latest_poll_list': expired_polls})


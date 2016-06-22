# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import HttpResponse, HttpResponseForbidden
import json, requests
from random import random
from pprint import pprint

PAGE_ACCESS_TOKEN = 'EAAPtuD3EFgoBAEkFrpxJ0iSvQr3G186xEz13GHu3uqgZAZAJdFKdCkOOKjJ8xFFA6gDsq2TLQpJqJmmRp8sZAlS4HflkuXgEbxau0yhUOxNwz6hB3lBLAf5yRywSg7vPR7k9XHNFCk3m8Vzu4n1XJLXSU7mZABGhGZAR7PgNI9E7NNH3ruy93'
VERIFY_TOKEN = '61581898'

bark = u'汪'

def index(request):
    return render(request, 'index.html', locals())

class ZuiBotView(generic.View):

    def get(self, request, *args, **kwargs):
        # return HttpResponse('What the fuck')
        # return HttpResponse("Hello World!")
        if request.GET['hub.verify_token'] == VERIFY_TOKEN:
            # pprint('what the ???')
            return HttpResponse(request.GET['hub.challenge'])

        else:
            # pprint('what the fuck')
            return HttpResponseForbidden()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_ACCESS_TOKEN
    n = len(recevied_message) >> 1
    if n < 2: n = 2
    maxl = round(random() * 10)
    msg = ''
    for i in range(n):
        msg += (bark * int(round(random() * maxl)) + ' ')
    msg = msg[:-1]
    if random() >= 0.5: msg += '!'
    elif random() >= 0.5: msg += '?'
    elif random() >= 0.5: msg += '~'
    if random() >= 0.5: msg += ';)'


    response_msg = json.dumps({"recipient":{"id":fbid},
                               "message":{"text":msg}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def test(request):
    return HttpResponse("Just for test")
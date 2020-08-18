from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque


diag, oil, tires = deque(), deque(), deque()
tickets = {'diagnostic': diag, 'change_oil': oil, 'inflate_tires': tires}
times = {'diagnostic': 30, 'change_oil': 2, 'inflate_tires': 5}
next = None

def get_next():
    global next
    if bool(tickets['change_oil']):
        next = tickets['change_oil'].pop()
    elif bool(tickets['inflate_tires']):
        next = tickets['inflate_tires'].pop()
    elif bool(tickets['diagnostic']):
        next = tickets['diagnostic'].pop()
    else:
        pass
    return next


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request,  'tickets/menu.html', {'problems':{
            'change_oil': 'Change oil',
            'inflate_tires': 'Inflate tires',
            'diagnostic': 'Get diagnostic test'
        }
        })

class TicketView(View):
    def get(self, request, service, *args, **kwargs):
        number = sum([len(x) for x in tickets.values()]) + 1
        oil_time = len(tickets['change_oil']) * times['change_oil']
        tire_time = len(tickets['inflate_tires']) * times['inflate_tires']
        diag_time = len(tickets['diagnostic']) * times['diagnostic']
        if service == 'change_oil':
            wait_time = oil_time
            tickets['change_oil'].appendleft(number)
        elif service == 'inflate_tires':
            wait_time = oil_time + tire_time
            tickets['inflate_tires'].appendleft(number)
        elif service == 'diagnostic':
            wait_time = oil_time + tire_time + diag_time
            tickets['diagnostic'].appendleft(number)
        else:
            wait_time = 0
        html = f'<div>Your number is {number}</div>' \
               f'<div>Please wait around {wait_time} minutes</div>'
        return HttpResponse(html)

class ProcessView(View):
    def get(self, request, *args, **kwargs):
        oil_q = len(tickets['change_oil'])
        tire_q = len(tickets['inflate_tires'])
        diag_q = len(tickets['diagnostic'])
        context = {'oil_q':oil_q, 'tire_q': tire_q, 'diag_q':diag_q}
        return render(request, 'tickets/operators.html', context=context)

    def post(self, request, *args, **kwargs):
        global next
        next = get_next()
        return redirect('/next', next)


class NextView(View):
    def get(self, request, *args, **kwargs):
        global next
        return render(request, 'tickets/next.html', context={'next': next})


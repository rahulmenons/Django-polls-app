from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import connections
from django.db.utils import OperationalError
from rest_framework.decorators import api_view
from rest_framework.response import Response
import psutil

@api_view(['GET'])
def alive(request):
    return Response({'status': 'alive'})

@api_view(['GET'])
def ready(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return Response({'status': 'not ready'}, status=503)
    return Response({'status': 'ready'})

@api_view(['GET'])
def health(request):
    cpu_percent = psutil.cpu_percent(interval=1)  # % CPU usage
    ram = psutil.virtual_memory()
    mem_percent = ram.percent                     # % RAM used
    mem_used_gb = round(ram.used / 1e9, 2)        # Used RAM in GB
    return Response({
        "cpu_usage_percent": cpu_percent,
        "ram_usage_percent": mem_percent,
        "ram_used_gb": mem_used_gb
    })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to the results page to prevent double-posting
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# 3 Views to be created index(all questions),detail(one question and choice),results.
#render takes template with dictionary and creates a webpage/HTML basically


def index(request):
    query = request.GET.get('q')
    if query:
        question_list = Question.objects.filter(question_text__icontains=query).order_by('-pub_date')
    else:
        question_list = Question.objects.order_by('-pub_date')

    paginator = Paginator(question_list, 5)  # Show 5 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'polls/index.html', {
        'page_obj': page_obj,
        'query': query
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

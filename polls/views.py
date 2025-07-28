from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    latest_question_list = Question.objects.order_by('-pub_date')
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request=request, template_name="polls/index.html", context={
#         "latest_question_list" : latest_question_list
#     })


# def detail(request, question_id):
#         question = get_object_or_404(Question, pk=question_id)
#         return render(request=request, template_name="polls/details.html", context={
#              "question": question
#         })


# def results(request, question_id):
#     question =  get_object_or_404(Question, pk = question_id)
#     return render(request=request, template_name="polls/results.html", context={
#          "question":question
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
         selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist) :
        return render(request=request, template_name="polls/details.html", context={
            "question" : question,   
            "error_message" : "No elegiste ninguna respuesta"}
            )     
    else:
         selected_choice.votes += 1
         selected_choice.save()
         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))     

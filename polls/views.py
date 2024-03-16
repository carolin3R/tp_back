from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponseRedirect, Http404, HttpResponse
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.db.models import F, Count
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from django.utils import timezone
from rest_framework.decorators import api_view
import logging
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)
@api_view(['GET'])
def IndexView(request):
    try:
        latest_question_list = Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct().order_by('-pub_date')[:5]
        data = {'latest_question_list': list(latest_question_list.values())}
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in IndexView: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
@api_view(['GET'])
def DetailView(request, question_id):
    if request.method == "GET":
        try:
            question = get_object_or_404(Question, pk=question_id)
            if not question.choice_set.exists():
                raise Http404("This question does not have any choices.")
            data = {'question': question.question_text, 'choices': list(question.choice_set.values())}
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Error in DetailView: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
@api_view(['GET'])
def ResultView(request, question_id):
    if request.method == "GET":
        try:
            question = get_object_or_404(Question, pk=question_id)
            if not question.choice_set.exists():
                raise Http404("This question does not have any choices.")
            data = {'question': question.question_text, 'choices': list(question.choice_set.values())}
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Error in ResultView: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
@csrf_exempt
def vote(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
        print("QUESTION IS", question)
        print("request is", request)
        choice_id = request.POST.get("choice")
        print("CHOICE ID IS", choice_id)
        if choice_id is None:
            # Handle the case where "choice" key is not present in request.POST
            print("The 'choice' field is missing from the form data.")
        else:
            selected_choice = question.choice_set.get(pk=(int(choice_id)))
            print("choice = ", selected_choice)
        print("does question choice exist", question.choice_set.exists())
        if not question.choice_set.exists():
            raise Http404("This question does not have any choices.")
        print("post request choice is ")
        print(request.POST["choice"])
        selected_choice = question.choice_set.get(pk=int(request.POST["choice"]))
        print("choice = ", selected_choice)
    except (KeyError, Choice.DoesNotExist) as e:
        if isinstance(e, KeyError):
            print("Key error occurred.")
        elif isinstance(e, Choice.DoesNotExist):
            print("Choice does not exist.")
        logger.error(f"Error in vote: {e}")
        return JsonResponse({"error": "You didn't select a choice."}, status=400)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return JsonResponse({"success": True, "redirect": reverse("polls:results", args=(question.id))})
    

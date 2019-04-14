from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Sport, Team, Employee
from django.http import JsonResponse


def index(request):
    context = {
        "teams": Team.objects.all()
    }
    return render(request, "tournament/index.html", context)


def bookscore(request):
    context = {
        "employees": Employee.objects.all(),
        "max_per_team": range(2),
        "max_team_per_event": range(2)
    }
    return render(request, "tournament/bookscore.html", context)


def autocomplete(request):
    if request.is_ajax():
        queryset = Employee.objects.all()
        list = []
        for i in queryset:
            list.append(str(i))
        data = {
            'list': list,
        }
        return JsonResponse(data)

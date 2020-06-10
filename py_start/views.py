from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def project_index(request):
    return render(request, "index.html", locals())


def pos_system_index(request):
    return render(request, "pos_system_index.html", locals())


def inner_index(request):
    return render(request, "inner_index.html", locals())


def inner_login_page(request):
    return render(request, "inner_login_page.html", locals())

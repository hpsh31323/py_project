from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def project_index(request):
    return render(request, "index.html", locals())


def pos_system_index(request):
    return render(request, "pos/pos_system_index.html", locals())


def manager_index(request):
    return render(request, "cms/manager_index.html", locals())


def inner_login_page(request):
    return render(request, "cms/inner_login_page.html", locals())



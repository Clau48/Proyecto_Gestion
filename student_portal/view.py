from datetime import datetime
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from course.models import Course

@login_required
def index(request):
    return render(request,'courses/categories.html',{})


def despedida(request):
    
    # return render(request,'student_portal')
    # dateNow = datetime.now()
    # documento1= """
    #     <h1> %s </h1>
    # """ % dateNow
    
    # # doc_externo = open("/home/jose/Documentos/hola.txt", "r")
    return render(request,'courses/allCourses.html',{})
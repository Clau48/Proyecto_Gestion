from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

def saludo(request):
    return HttpResponse("Hola alumnos esta es nuestra primera pagina con Django")


def despedida(request):
    
    # return render(request,'student_portal')
    # dateNow = datetime.now()
    # documento1= """
    #     <h1> %s </h1>
    # """ % dateNow
    
    # # doc_externo = open("/home/jose/Documentos/hola.txt", "r")
    return render(request,'courses/allCourses.html',{})

def showCourse(request):
    return render(request,'courses/categories.html',{})
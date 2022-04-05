from datetime import datetime
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from course.models import Course

@login_required
def index(request):
    return render(request,'courses/categories.html',{})

def showCourse(request):
    courses = Course.objects.filter()    
    context = {
        'courses': courses,
    }
    return render(request,'courses/categories.html',context)

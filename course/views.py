from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from course.models import Course
from course.forms import NewCourseForm

# CONSTANTES

MIS_CURSOS_URL = 'course/mycourses.html'

# Create your views here.

@login_required
def index(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user)
    for course in courses:
        print(course.id, course.title)

    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

def initialize_arrays(courses, u_courses, times):
    for course in courses:
        time = course.time_start
        if time not in times:
            times.append(time)
            u_courses.append([])
    times.sort

def fill_array(u_courses, times):
    for i in range(0, len(times)):
        u_courses[i].sort(key=lambda c: int(c.day))
        j = 0
        while j < 7:
            try:
                if int(u_courses[i][j].day) != (j + 1):
                    u_courses[i].insert(j, None)
            except Exception:
                u_courses[i].append(None)
            j += 1
 
def new_course(request):
    user = request.user
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            time_start = form.cleaned_data.get('time_start')
            time_end = form.cleaned_data.get('time_end')
            category = form.cleaned_data.get('category')
            syllabus = form.cleaned_data.get('syllabus')
            Course.objects.create(picture=picture, title=title, description=description, 
            time_start=time_start, time_end=time_end, category=category,
            syllabus=syllabus, user=user)
            
            courses = Course.objects.filter(user=user)
            messages.success(request, '¡El curso ha sido creado con éxito!')
            return render(request, MIS_CURSOS_URL, {'courses': courses})
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'course/newcourse.html', context)



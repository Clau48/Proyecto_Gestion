from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from course.models import Assignment, Course, Homework, Post
from course.forms import NewCourseForm, NewPostForm
from django.contrib import messages
import datetime

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
            time_start = form.cleaned_data.get('time_start')
            time_end = form.cleaned_data.get('time_end')

            if not ValidateTime(request, time_start, time_end):
                context = {'form': form}
                return render(request, 'courses/newcourse.html', context)

            picture = form.cleaned_data.get('picture')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            syllabus = form.cleaned_data.get('syllabus')
            Course.objects.create(picture=picture, title=title, description=description, 
            time_start=time_start, time_end=time_end,
            syllabus=syllabus, user=user)
            return redirect('../../courses/')
    else:
        form = NewCourseForm()

    context = {
        'form': form,
    }

    return render(request, 'courses/newcourse.html', context)

def ValidateTime(request, time_start, time_end):
    ts = str(time_start).split(":")
    te = str(time_end).split(":")
    confirmation = True

    if ts[1] != "00" or te[1] != "00":
        messages.warning(request, 'La hora de inicio y cierre deben de darse en horas en punto. ' + 
            'Ejm: "Inicio - 8:00 y Fin - 9:00"')
        confirmation = False
    if int(ts[0]) > int(te[0]):
        messages.warning(request, 'La hora de inicio no puede pasar de la hora de cierre.')
        confirmation = False

    return confirmation

def show_mycourses(request):
    courses = Course.objects.filter(user=request.user)    
    context = {
        'courses': courses,
    }    
    return render(request, 'courses/mycourses.html', context)
def showCourse(request):
    courses = Course.objects.filter()    
    context = {
        'courses': courses,
    }
    return render(request,'courses/categories.html',context)


def NewPost(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewPostForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                file = form.cleaned_data.get('file')
                post = Post.objects.create(title=title, content=content, file=file, course_id=course_id)
                course.posts.add(post)
                course.save()
                return redirect('show_posts', course_id=course_id)
        else:
            form = NewPostForm()

    context = {
        'form': form,
    }
    return render(request, 'post/newpost.html', context)

def show_posts(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    posts = Post.objects.filter(course_id=course_id)
    assignmentValidate = Assignment.objects.filter(post_ptr_id__in=posts)
    homeworkUser = Homework.objects.filter(assignment__in=assignmentValidate,student_id=request.user.id)
    teacher_mode = False
    if user == course.user:
        teacher_mode = True
        
    context = {
        'teacher_mode': teacher_mode,
        'course': course,
        'posts': posts,
        'homeworkUser': homeworkUser,
    }

    return render(request, 'post/posts.html', context)

@login_required
def send_homework(request, course_id,post_id):
    
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    post = Post.objects.get(id=post_id)
    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    context = {
        'teacher_mode': teacher_mode,
        'course': course,
        'post': post
    }    
    return render(request, 'post/send_homework.html',context);

@login_required
def send_homework_post(request,course_id,post_id):
    if request.method == 'POST':
        try:
            postValidate = Post.objects.get(id=post_id)
            assignmentValidate = Assignment.objects.get(post_ptr_id=postValidate)
            exists = Homework.objects.filter(assignment_id=assignmentValidate.post_ptr_id,student_id=request.user.id)
            if exists:
                messages.warning(request, 'No se pudo enviar, ya has enviado tu material para esta tarea.')
                return redirect('show_posts', course_id=course_id)
            description = request.POST['description']
            file = request.POST['file']
            comentary = request.POST['comentary']
            idAssigment = post_id   
            grade = 0
            idUser = request.user.id
            date = datetime.datetime.now()
            assignment = Assignment.objects.get(post_ptr_id=idAssigment)
            homework = Homework.objects.create(grade=grade,assignment=assignment ,student=request.user, description_short=description, comentary=comentary,turn_in_timestamp=date,file=file)                     
            messages.success(request, 'Entregado correctamente')
            return redirect('/course/%s/posts' % course_id)            
        except :
            messages.error(request, 'Todos los campos deben ser rellenados')
            return redirect('send_homework')
            
        
    else:
        return redirect('/courses/')
        
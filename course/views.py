from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import *
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib.auth.models import User
from django.db.models import Q
from course.models import Assignment, Course, Homework, Post
from course.forms import NewAssignmentForm, NewCourseForm, NewPostForm
import datetime
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from course.models import Course, Post, Course_User
from course.forms import NewCourseForm, NewPostForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

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
 
@login_required
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

@login_required
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


@login_required
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

@login_required
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
        
@login_required
def show_course_description(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    is_registered = Course_User.objects.filter(course=course_id, user=user.id).all()
    is_owner = (user == course.user)
    context = {
        'course': course,
        'user': user,
        'is_registered': is_registered,
        'is_owner': is_owner
    }

    return render(request, 'courses/course.html', context)

def send_link_course(user, domain, course, to_email):
    subject = 'Invitación a curso'
    html_message = render_to_string("courses/email_invitation.html", {
        "domain": domain,
        "user": user,
        "course": course,
        "codeInvitation": str(course.codeinvitation)
    },)
    from_email = user.email

    plain_message = strip_tags(html_message)
    return send_mail(subject, plain_message, from_email , [to_email], html_message=html_message)

@login_required
def sendInscriptionLink(request, course_id):
    if request.method == 'POST':
        to_email = request.POST.get('to_email')

        email_exists = User.objects.filter(email=to_email).all()
        if not email_exists:
            return HttpResponseBadRequest('Error al enviar correo: no pertenece a un usuario registrado')

        if to_email:
            user_owner =  request.user
            domain = get_current_site(request).domain
            course = Course.objects.get(id=course_id)
            
            send_link_course(user_owner, domain, course, to_email)

            return HttpResponse('Correo enviado a ' + to_email)
        else:
            return HttpResponseBadRequest('Email vacio')

def usersInCourse(request, course_id):
    users_query = Course_User.objects.filter(course=course_id).all()
    data = []
    for user in users_query:
        user_dict = {
            "name": str(user.user),
            "email": str(user.user.email),
            "picture": str(user.user.profile.picture)
        }
        data.append(user_dict)
    return JsonResponse({'users': data})

@login_required
def inscriptionLink(request, codeInvitation):
    try:
        course = Course.objects.get(codeinvitation=codeInvitation)
        already_inscription = Course_User.objects.filter(user=request.user.id, course=course.id)     
        if already_inscription:
            messages.error(request, 'Ya estas inscrito en este curso')
            return redirect('/user/inscription/')
        else:  
            Course_User.objects.create(user=request.user, course=course)
            messages.success(request, 'Inscripcion correcta')
            return redirect('/user/inscription/')
    except:
        return HttpResponse('Link de activación inválido')
    
    
@login_required
def show_calification(request, course_id):
    # try:    
        posts = Post.objects.filter(course_id=course_id)
        assignmentValidate = Assignment.objects.filter(post_ptr_id__in=posts)
        homework = Homework.objects.filter(assignment__in=assignmentValidate, student_id=request.user.id)
        data = assignmentValidate
        data_prom = 0
        quantity_prom = 0
        for d in data:
            d.homework = homework.filter(assignment_id=d.post_ptr_id, student_id=request.user.id).first()
            d.post = posts.filter(id=d.post_ptr_id)
            if d.homework and d.homework.grade != 0:
                data_prom += d.homework.grade
                quantity_prom += 1
        quantity_prom = quantity_prom == 0 if 1 else quantity_prom
        data_prom = data_prom / quantity_prom
        data_aditional = {}
        data_aditional['prom'] = data_prom
        context = {
            'data': data,
            'data_aditional': data_aditional,
        }       
        return render(request, 'courses/calification.html',context)
        
    # except:
        
        # messages.error(request, 'Error, no se pudo cargar la pagina')
        # return redirect('/course/%s/posts' % course_id)            

def send_notification_new_asignement(user, domain, assignment, course, to_emails):
    subject = f'Se ha agregado una nueva tarea en el curso {course.title}'
    html_message = render_to_string("assignment/tarea_notificacion.html", {
        "domain": domain,
        "user": user,
        "course": course,
        "assignment": assignment
    },)
    from_email = user.email

    plain_message = strip_tags(html_message)
    return send_mail(subject, plain_message, from_email , to_emails, html_message=html_message)
        
def new_assignment(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                due_datetime = form.cleaned_data.get('due_datetime')
                file = form.cleaned_data.get('file')
                is_asgmt = form.cleaned_data.get('is_asgmt')
                
                post_asgmt = Assignment.objects.create(title=title, content=content, file=file, course_id=course_id, due_datetime=due_datetime, is_asgmt=is_asgmt)
                course.posts.add(post_asgmt)

                if is_asgmt:
                    users_in_course = Course_User.objects.filter(course=course_id).all()
                    to_emails = [] 

                    for u in users_in_course:
                        to_emails.append(str(u.user.email))

                    domain = get_current_site(request).domain
                    send_notification_new_asignement(user, domain, post_asgmt, course, to_emails)
                    pass

                course.save()
                return redirect('show_posts',course_id=course_id)
        else:
            form = NewAssignmentForm()

    context = {
        'form': form,
    }

    return render(request, 'assignment/newassignment.html', context)


def edit_assignment(request, course_id, assignment_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES, instance=assignment)
            if form.is_valid():
                assignment.title = form.cleaned_data.get('title')
                assignment.content = form.cleaned_data.get('content')
                assignment.due_datetime = form.cleaned_data.get('due_datetime')
                assignment.file = form.cleaned_data.get('file')
                assignment.save()
                return redirect('show_posts', course_id=course_id)
        else:
            form = NewAssignmentForm(instance=assignment)
            form.file = assignment.file

    context = {
        'form': form,
        'course_id': course_id,
        'assignment_id': assignment_id
    }
    return render(request, 'assignment/newassignment.html', context)

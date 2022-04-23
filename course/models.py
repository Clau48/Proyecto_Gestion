from django.db import models
from django.core import validators
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
from django.core import validators

def user_directory_path(instance, filename):
    # THis file will be uploaded to MEDIA_ROOT /the user_(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def course_storage_path(instance, filename):
    filename = 'portada.jpg'
    id = len(Course.objects.all()) + 1
    return f'courses/{id}/banner/{filename}'

def post_storage_path(instance, filename):
    id = len(Post.objects.filter(course=instance.course)) + 1
    return f'{instance.course.get_storage_path()}/posts/{id}/{filename}'

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    
class Course(models.Model):
    picture = models.ImageField(upload_to=course_storage_path)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    DAY_CHOICES = [
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miércoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sábado'),
        ('DO', 'Domingo')
    ]
    day = models.CharField(
        max_length=2,
        choices=DAY_CHOICES,
        default='LU'
    )
    time_start = models.TimeField()
    time_end = models.TimeField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    syllabus = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_owner')
    codeinvitation = models.UUIDField(unique=True , default=uuid.uuid4, editable=False)
    enrolled = models.ManyToManyField(User)
    deleted = models.BooleanField(default=False)
    # modules = models.ManyToManyField(Module)
    # questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title    
    
    def get_storage_path(self):
        return f'courses/{self.pk}'    
    
class Course_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    course = models.ForeignKey(Course, on_delete=models.CASCADE )
    def get_storage_path(self):
        return f'courses/{self.pk}'

class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=300, null=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=post_storage_path, null=True, blank=True)
    is_asgmt = models.BooleanField(default=False)
    def get_storage_path(self):
        return f'{self.course.get_storage_path()}/posts/{self.pk}'
		
class Assignment(Post):
    due_datetime = models.DateTimeField()

def homework_storage_path(instance, filename):
    id = len(Homework.objects.filter(assignment=instance.assignment)) + 1
    return f'{instance.assignment.get_storage_path()}/homeworks/{id}/{filename}'

class Homework(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='homeworks')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    turn_in_timestamp = models.DateTimeField(auto_now=True)
    description_short = models.CharField(max_length=300,null=True,default=None)    
    comentary = models.CharField(max_length=1000, null=True,default=None)    
    grade = models.IntegerField(
        validators=[
            validators.MaxValueValidator(20),
            validators.MinValueValidator(-1)
        ],
        default = -1
    )
    now_calification = models.BooleanField(default=False)
    file = models.FileField(upload_to=homework_storage_path, null=True, blank=True)

    def get_storage_path(self):
        return f'{self.assignment.get_storage_path()}/homeworks/{self.pk}'

class Team(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='team')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team')
    grupe_name = models.CharField(max_length=200)
    grupe_number = models.IntegerField(default=0)
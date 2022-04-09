from pyexpat import model
from django import forms
from course.models import *

# from ckeditor.widgets import CKEditorWidget

class NewCourseForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Titulo'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Descripcion'}), required=True)
	day = forms.ChoiceField(choices=Course.DAY_CHOICES, required=False)
	time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	syllabus = forms.CharField()

	class Meta:
		model = Course
		fields = ('picture', 'title', 'description', 'day', 'time_start', 'time_end', 'syllabus')


class InscriptionForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Titulo'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Descripcion'}), required=True)

	class Meta:
		model = Course
		fields = ('picture', 'title', 'description', 'day', 'time_start', 'time_end', 'syllabus')
		
class NewPostForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	content = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=False)
	file = forms.FileField(required=False)
	class Meta:
		model = Post
		fields = ('title', 'content','file')

class NewAssignmentForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	content = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=False)
	file = forms.FileField(required=False)
	due_datetime = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
	is_asgmt = forms.BooleanField(required=True) 

	class Meta:
		model = Assignment
		fields = ('title', 'content', 'file', 'due_datetime', 'is_asgmt')

from django import forms
from course.models import Course, Post
from cloudinary.forms import CloudinaryFileField
from ckeditor.widgets import CKEditorWidget


class NewCourseForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Titulo'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Descripcion'}), required=True)
	day = forms.ChoiceField(choices=Course.DAY_CHOICES, required=True)
	time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	syllabus = forms.CharField()

	class Meta:
		model = Course
		fields = ('picture', 'title', 'description', 'day', 'time_start', 'time_end', 'syllabus')

class NewPostForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Titulo'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate','placeholder':'Descripcion'}), required=True)
	file = CloudinaryFileField(options={'folder' : 'media/courses/posts/'})
	class Meta:
		model = Post
		fields = ('title', 'description','file')
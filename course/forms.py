from django import forms
from course.models import Course


class NewCourseForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	day = forms.ChoiceField(choices=Course.DAY_CHOICES, required=True)
	time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), required=True)
	syllabus = forms.CharField()

	class Meta:
		model = Course
		fields = ('picture', 'title', 'description', 'day', 'time_start', 'time_end', 'syllabus')

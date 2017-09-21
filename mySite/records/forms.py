# records/forms.py

from PIL import Image
from django import forms
from django.forms import Textarea

# Create your forms here.
from mySite.master.models import Job
from .models import Person, Event, Evidence

class PersonForm(forms.ModelForm):
    jobs = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), 
            widget=forms.CheckboxSelectMultiple)
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tag을 입력해 주세요.'}))
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    picture = forms.FileField(required=False)

    class Meta:
        model = Person
        fields = ['name', 'nick_name', 'birth_year', 'jobs', 'picture', 'url', 'x', 'y', 'width', 'height', ]
        widgets = {
            'picture': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        person = super(PersonForm, self).save()

        if not person.picture:
            return person 
            
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        image = Image.open(person.picture)
        cropped_image = image.crop((x, y, width+x, height+y))
        resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
        resized_image.save(person.picture.path)

        return person


class EventForm(forms.ModelForm):
    person = forms.IntegerField(widget=forms.HiddenInput())
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tag을 입력해 주세요.'}),
                            help_text='입력할 때 ,을 이용해 구분해 주시기 바랍니다.')
    class Meta:
        model = Event
        fields = ['name', 'content', 'category', 'person']
        widgets = {
            'content': Textarea(attrs={'rows': 3}),
        }

class EvidenceForm(forms.Form):
    url = forms.URLField()


class PersonEvidenceForm(forms.ModelForm):
    personevent = forms.IntegerField(widget=forms.HiddenInput())
    news = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Evidence
        fields = ['personevent', 'news']





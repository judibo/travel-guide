from django.forms import ModelForm, Form, CharField, PasswordInput, BooleanField
from .models import Comment, BucketSpot

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class CheckDone(ModelForm):
    done = BooleanField()

    class Meta:
        model = BucketSpot
        fields = ['done']
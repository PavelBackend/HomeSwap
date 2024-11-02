from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "image", "content", "available"]

    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите заголовок"}
        ),
    )

    image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    content = forms.CharField(
        max_length=1500,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Введите содержание поста"}
        ),
    )

    available = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

from django import forms
from .models import Posts

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image_url', 'content', 'available']
    
    # Настраиваем виджет для каждого поля, если нужно
    title = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'})
    )
    
    image_url = forms.URLField(
        required=False,  # Поле не обязательное
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите URL изображения'})
    )
    
    content = forms.CharField(
        max_length=1500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите содержание поста'})
    )
    
    available = forms.BooleanField(
        required=False,  # Поле не обязательное
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

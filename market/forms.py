from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form

from .models import Author, Product


class AuthorLoginForm(Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AuthorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    password2 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    avatar = forms.FileField()

    def save(self, commit=True):
        user = super().save(commit)
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 == password2:
            user.set_password(password1)
            user.save()
        else:
            raise ValidationError("Passwords must be match")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Author
        fields = ("username", "first_name", "last_name", "password1", "password2", "email", "avatar")


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'ends_in', 'product_type']
        widgets = {
            'ends_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(
                attrs={'rows': 5, 'cols': 20, 'class': 'form-control', 'placeholder': 'Description', 'required': True,
                       'autofocus': True, 'id': 'description'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'ends_in', 'product_type']
        widgets = {
            'ends_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(
                attrs={'rows': 5, 'cols': 20, 'class': 'form-control', 'placeholder': 'Description', 'required': True,
                       'autofocus': True, 'id': 'description'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'ends_in', 'product_type', 'name',]

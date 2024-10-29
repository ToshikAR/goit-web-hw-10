from django import forms
from django.forms import (
    CharField,
    DateField,
    DateInput,
    ModelChoiceField,
    Select,
    TextInput,
    Textarea,
    ModelMultipleChoiceField,
    SelectMultiple,
)

from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    fullname = CharField(
        max_length=100,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Fullname"}),
    )
    born_date = DateField(
        required=True,
        widget=DateInput(
            attrs={"class": "form-control", "placeholder": "Born Date"},
        ),
    )
    born_location = CharField(
        max_length=150,
        min_length=3,
        required=True,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "Born Location"},
        ),
    )
    description = CharField(
        required=True,
        widget=Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "style": "height: 200px;",
            }
        ),
    )

    class Meta:
        model = Author
        fields = ("fullname", "born_date", "born_location", "description")


class QuoteForm(forms.ModelForm):
    author = ModelChoiceField(
        queryset=Author.objects.all(), required=True, widget=Select(attrs={"class": "form-select"})
    )
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=SelectMultiple(
            attrs={
                "class": "form-select",
                "style": "height: 150px;",
            }
        ),
    )
    quote = CharField(
        required=True,
        widget=Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Quote",
                "style": "height: 100px;",
            }
        ),
    )

    class Meta:
        model = Quote
        fields = ("author", "tags", "quote")


class TagForm(forms.ModelForm):
    name = CharField(
        required=True, widget=Textarea(attrs={"class": "form-control", "placeholder": "Tag"})
    )

    class Meta:
        model = Tag
        fields = ("name",)

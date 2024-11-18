from unittest import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count


from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm, TagForm
from .utils import get_mongodb, fill_start

from .scraping.scrap import start_scrap


db = get_mongodb()


# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    top_tags = Tag.objects.annotate(quote_count=Count("quote")).order_by("-quote_count")[:10]
    context = {
        "quotes": quotes_on_page,
        "top_tags": top_tags,
    }

    return render(request, "quotes_app/index.html", context)


def author(request, id_=1):
    author = Author.objects.get(id=id_)
    return render(request, "quotes_app/author.html", context={"author": author})


def tags(request, tag_=""):
    quotes = Quote.objects.filter(tags__name__in=[tag_]).order_by("id").all()
    context = {
        "tag_": tag_,
        "quotes": quotes,
    }
    return render(request, "quotes_app/tags.html", context)


class AuthorView(View):
    template_name = "quotes_app/author_add.html"
    form_class = AuthorForm
    form_class1 = TagForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="quotes_app:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={
                "form": self.form_class,
                "form1": self.form_class1,
            },
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "form1": self.form_class1,
            },
        )


class QuoteView(View):
    template_name = "quotes_app/quote_add.html"
    form_class = QuoteForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="quotes_app:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return render(request, self.template_name, context={"form": form})


class TagView(View):
    template_name = "quotes_app/tag_add.html"
    form_class = TagForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="quotes_app:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return render(request, self.template_name, {"form": form})


@login_required
def fillAll(request):
    fill_start()
    return redirect(to="quotes_app:root")


@login_required
def scrap(request):
    start_scrap()
    return redirect(to="quotes_app:root")


def testing(request):
    template = loader.get_template("user_app/usertest.html")
    return HttpResponse(template.render())

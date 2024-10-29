from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from django.contrib import messages


from django.contrib.auth.views import LogoutView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
class RegisterView(View):
    template_name = "user_app/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes_app:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"{username} account was created")
            return redirect(to="user_app:login")
        return render(request, self.template_name, {"form": form})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes_app:root")

    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is None:
            messages.error(request, f"Username or password didn't match")
            return redirect(to="user_app:login")

        login(request, user)
        return redirect(to="quotes_app:root")

    return render(request, "user_app/login.html", context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return render(request, "user_app/logout.html", context={})

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from accounts.models import Cook
from accounts.forms import RegisterForm


class CooksListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Cook
    success_url = reverse_lazy("accounts:cook-list")


class RegisterView(CreateView):
    model = Cook
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("kitchen:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

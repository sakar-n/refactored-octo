from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView , FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("task")

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class  = UserCreationForm
    redirect_authenticated_user = False
    success_url = reverse_lazy("task")

    def form_valid(self, form): 
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    
    


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(
                title__icontains= search_input)
        context ['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"
    redirect_authenticated_user = True
    
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404("You do not have permission to view this task.")
        return super().dispatch(request, *args, **kwargs)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description','complete']
    
    success_url = reverse_lazy("task")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
 
    


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy("task")
    redirect_authenticated_user = False
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404("You do not have permission to view this task.")
        return super().dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task")
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            raise Http404("You do not have permission to view this task.")
        return super().dispatch(request, *args, **kwargs)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
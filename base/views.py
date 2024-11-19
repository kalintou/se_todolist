from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.db.models import Q  # 添加这个导入，用于复杂查询
from django.utils import timezone  # 如果需要基于当前时间进行排序

from django.db.models import Case, When, IntegerField

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm

def custom_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        # 处理搜索功能
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)

        # 处理排序
        sort_by = self.request.GET.get('sort', 'manual')  # 默认按手动排序
        if sort_by == 'due_date_asc':
            queryset = queryset.order_by('due_date')
        elif sort_by == 'due_date_desc':
            queryset = queryset.order_by('-due_date')
        elif sort_by == 'created_asc':
            queryset = queryset.order_by('created')
        elif sort_by == 'created_desc':
            queryset = queryset.order_by('-created')
        elif sort_by == 'priority_asc':
            queryset = queryset.annotate(
                priority_value=Case(
                    When(priority='低', then=1),
                    When(priority='中', then=2),
                    When(priority='高', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('priority_value')
        elif sort_by == 'priority_desc':
            queryset = queryset.annotate(
                priority_value=Case(
                    When(priority='低', then=1),
                    When(priority='中', then=2),
                    When(priority='高', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('-priority_value')
        else:
            # 使用显式添加的 'order' 字段进行排序
            queryset = queryset.order_by('order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object_list  # 使用已经获取的 queryset
        context['count'] = tasks.filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area', '')
        context['current_sort'] = self.request.GET.get('sort', 'manual')
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'
    title = '创建新任务'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'
    title = '更新任务'


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                for idx, task_id in enumerate(positionList):
                    Task.objects.filter(id=task_id, user=request.user).update(order=idx)

        return redirect(reverse_lazy('tasks'))
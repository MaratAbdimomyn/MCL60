from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user_list')

    def send_verify_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}')
        message = f'Дарова, {user.username}! Перейдите по ссылке ниже для подтверждения почты: {verify_url}'
        send_mail('Подтверждение почты', message, 'abdimomynmarat@gmail.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()
        self.send_verify_email(user)
        return response

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class VerificationSuccess(TemplateView):
    template_name = 'verificationsuccess.html'

class VerificationError(TemplateView):
    template_name = 'verificationerror.html'

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verificationsuccess')
        else:
            return redirect('verificationerror')

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('post_list')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=False')

class Logout(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CreateCategoryView(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'category_create.html'
    success_url = reverse_lazy('category_list')

class DetailCategoryView(DetailView):
    model = Category
    template_name = 'category_about.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs: Any):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.GET.get("category"):
            cat = Category.objects.get(name=self.request.GET['category'])
            print(cat)
            qs = Post.objects.filter(category = cat)
            return qs
        else:
            return Post.objects.all()
        """elif:
            self.request.GET.get("category"):
            cat = Category.objects.get(name=self.request.GET['category'])
            if cat == 'Cars':
                qs = Post.objects.filter(category.parent = cat)"""

    def get_context_data(self, **kwargs: Any):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCategoryForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCategoryForm
    template_name = 'post_update.html'
    success_url = reverse_lazy('post_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class DetailPostView(DetailView):
    model = Post
    template_name = 'post_about.html'
    context_object_name = 'post'

class DeletePostView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post_delete_confirm'
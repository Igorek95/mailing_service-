import random

from django.forms.models import BaseModelForm
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django_tables2 import SingleTableView

from blog.models import BlogEntry
from mailing.models import Client, EmailFilling, EmailSubscribtion
from mailing.permissions import is_creator, is_manager, is_su
from mailing.tables import ClientTable, EmailFillingTable, EmailSubscribtionTable, UserTable
from mailing.forms import (ClientForm,
                                      EmailFillingForm,
                                      EmailSubscribtionFormAdmin,
                                      EmailSubscribtionFormUser,
                                      EmailSubscribtionFormManager)
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

from users.models import User


def home(request):

    page_data = dict()

    page_data['sub_sum'] = EmailSubscribtion.objects.count()
    page_data['active_sub_sum'] = EmailSubscribtion.objects.filter(
        is_enabled='enabled').count()
    page_data['client_sum'] = Client.objects.count()

    blogentries_pk = list(BlogEntry.objects.filter(
        is_published=True).values_list('pk', flat=True))
    if len(blogentries_pk) <= 3:
        page_data['blog_entries'] = BlogEntry.objects.filter(is_published=True)
    else:
        random.shuffle(blogentries_pk)
        page_data['blog_entries'] = BlogEntry.objects. \
            filter(is_published=True, pk__in=blogentries_pk[:3])

    return render(request, 'mailing/home.html', context=page_data)


def contact(request):
    return render(request, 'mailing/contact.html')


def about(request):
    return render(request, 'mailing/about.html')


def email_distribution_menu(request):
    return render(request, 'mailing/subscribtion_menu.html')


class ManagerTableView(LoginRequiredMixin, UserPassesTestMixin, SingleTableView):
    model = User
    table_class = UserTable
    template_name = 'mailing/user_table.html'

    def test_func(self):
        return is_manager(self.request.user) or is_su(self.request.user)

    def get_queryset(self):
        if is_su(self.request.user):
            return super().get_queryset()
        else:
            return User.objects.filter(is_superuser=False)


@user_passes_test(lambda u: is_manager(u) or is_su(u))
def block_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_superuser:
        return render(request, 'mailing/404.html')
    user.is_active = False
    user.email_verification_token = 'blocked'
    user.save()
    return redirect('mailing:manager_menu')


@user_passes_test(lambda u: is_manager(u) or is_su(u))
def unblock_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_superuser:
        return render(request, 'mailing/404.html')
    user.is_active = True
    user.email_verification_token = 'unblocked'
    user.save()
    return redirect('mailing:manager_menu')


class ClientTableView(LoginRequiredMixin, SingleTableView):
    model = Client
    table_class = ClientTable
    template_name = 'mailing/client_table.html'

    def get_queryset(self):
        if is_su(self.request.user):
            return super().get_queryset()
        else:
            return self.model.objects.filter(user=self.request.user)


class EmailFillingTableView(LoginRequiredMixin, SingleTableView):
    model = EmailFilling
    table_class = EmailFillingTable
    template_name = 'mailing/message_table.html'


class EmailSubscribtionTableView(LoginRequiredMixin, SingleTableView):
    model = EmailSubscribtion
    table_class = EmailSubscribtionTable
    template_name = 'mailing/mailing_table.html'

    def get_queryset(self):
        if is_manager(self.request.user) or is_su(self.request.user):
            return super().get_queryset()
        else:
            return self.model.objects.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:clients')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Добавить'
        return context


class EmailFillingCreateView(LoginRequiredMixin, CreateView):
    model = EmailFilling
    form_class = EmailFillingForm
    template_name = 'mailing/message_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:mail_templates')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Добавить'
        return context


class EmailSubscribtionCreateView(LoginRequiredMixin, CreateView):
    model = EmailSubscribtion
    template_name = 'mailing/mailing_form.html'

    def get_form_class(self):
        if is_su(self.request.user):
            return EmailSubscribtionFormAdmin
        if not is_su(self.request.user):
            modelform = EmailSubscribtionFormUser
            modelform.base_fields['client'].limit_choices_to = {
                'user': self.request.user}
        return modelform

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:distributions_detail', args=(self.object.pk,))

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Добавить'
        return context


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or \
            is_su(self.request.user)

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Изменить'
        return context


class EmailFillingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmailFilling
    form_class = EmailFillingForm
    template_name = 'mailing/message_form.html'

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or \
            is_su(self.request.user)

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:templates_detail', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Изменить'
        return context


class EmailSubscribtionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmailSubscribtion
    template_name = 'mailing/mailing_form.html'

    def test_func(self):
        return is_manager(self.request.user) or \
            is_creator(self.get_object().user, self.request.user) or \
            is_su(self.request.user)

    def get_form_class(self):
        if is_su(self.request.user):
            return EmailSubscribtionFormAdmin
        if is_creator(self.get_object().user, self.request.user):
            modelform = EmailSubscribtionFormUser
            modelform.base_fields['client'].limit_choices_to = {
                'user': self.request.user}
            return modelform
        elif is_manager(self.request.user):
            return EmailSubscribtionFormManager

    def get_success_url(self, *args, **kwargs):
        return reverse('mailing:distributions_detail', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Изменить'
        return context


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_detail.html'

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or is_su(self.request.user)


class EmailFillingDetailView(LoginRequiredMixin, DetailView):
    model = EmailFilling
    form_class = EmailFillingForm
    template_name = 'mailing/message_detail.html'


class EmailSubscribtionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = EmailSubscribtion
    template_name = 'mailing/mailing_detail.html'

    def test_func(self):
        return is_manager(self.request.user) or \
            is_creator(self.get_object().user, self.request.user) or \
            is_su(self.request.user)


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:clients')

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or is_su(self.request.user)


class EmailFillingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailFilling
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:mail_templates')

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or is_su(self.request.user)


class EmailSubscribtionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmailSubscribtion
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mail_distributions')

    def test_func(self):
        return is_creator(self.get_object().user, self.request.user) or is_su(self.request.user)
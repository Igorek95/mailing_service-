from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Client, Mailing, Message, MailingLog
from .forms import MailingForm, MessageForm
from .services import send_messages


def home(request):
    return render(request, 'mailing/home.html')


def contact(request):
    return render(request, 'mailing/contact.html')


def about(request):
    return render(request,'mailing/about.html')
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('client-list')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('client-list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'





class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing-list')


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing-list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing-list')


class MailingSendView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_send.html'
    fields = []

    def form_valid(self, form):
        mailing = form.instance
        send_messages(mailing)
        mailing.status = 'started'
        mailing.save()
        return redirect('mailing-list')


class MailingDetailView(ListView):
    model = Message
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'messages'

    def get_queryset(self):
        mailing_id = self.kwargs['pk']
        return Message.objects.filter(mailing_id=mailing_id)

class MessageListView(ListView):
    model = Message
    template_name ='mailing/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing/message_form.html'
    form_class = MessageForm

    def form_valid(self, form):
        mailing_id = self.kwargs['mailing_id']
        form.instance.mailing_id = mailing_id
        return super().form_valid(form)

    def get_success_url(self):
        mailing_id = self.kwargs['mailing_id']
        return reverse_lazy('mailing-detail', args=[mailing_id])


class MessageUpdateView(UpdateView):
    model = Message
    template_name ='mailing/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('message-list')


class MessageDetailView(ListView):
    model = Message
    template_name ='mailing/message_detail.html'
    context_object_name ='messages'

    def get_queryset(self):
        message_id = self.kwargs['pk']
        return Message.objects.filter(pk=message_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.kwargs['pk']
        context['message'] = Message.objects.get(pk=message_id)
        return context


class MessageDeleteView(DeleteView):
    model = Message
    template_name ='mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message-list')




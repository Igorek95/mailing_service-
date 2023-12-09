from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import MailingForm, MessageForm, ClientForm
from .models import Client, Mailing, Message


def home(request):
    return render(request, 'mailing/home.html')


def contact(request):
    return render(request, 'mailing/contact.html')


def about(request):
    return render(request, 'mailing/about.html')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client-list')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'clients_detail'



class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:client-list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client-list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    template_name = 'mailing/mailing_form.html'

    def get(self, request, *args, **kwargs):
        form = MailingForm(initial={'status': 'Создана'})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MailingForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.status = request.POST['status']
            form.save()
            return redirect('mailing:mailing_list')
        else:
            result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
        return render(request, self.template_name, {'form': form, 'result': result})


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSendView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


from django.shortcuts import get_object_or_404

class MailingDetailView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        messages = Message.objects.filter(mailing=mailing)
        context['mailing'] = mailing
        context['messages'] = messages
        return context



class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    template_name = 'mailing/message_form.html'

    def get(self, request, *args, **kwargs):
        form = MessageForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailing:message_list')  # переход на страницу со всеми сообщениями
        else:
            result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
        return render(request, self.template_name, {'form': form, 'result': result})


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(ListView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'messages'

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
    template_name = 'mailing/message_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('mailing:message_list')

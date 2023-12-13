from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import EntryForm
from blog.models import BlogEntry


class EntryCreateView(PermissionRequiredMixin, CreateView):
    model = BlogEntry
    form_class = EntryForm
    template_name = 'blog/add_blog_entry.html'
    success_url = 'list_entry'
    permission_required = "blog.add_blogentry"

    def post(self, request, *args, **kwargs):
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            saved_form = form.save()
            saved_form.entry_slug = slugify(
                saved_form.entry_title)
            saved_form.user = request.user
            saved_form.save()
            result = "<h5 style='background-color: #00b91f; color: black; border-radius: 7px; height: 30px; text-align: center;'>Запись добавлена!</h5>"
            form = EntryForm()
        else:
            result = "<h5 style='background-color: #a50000; color: black; border-radius: 7px; height: 30px; text-align: center;'>Неправильно заполнены данные!</h5>"
        return render(request, self.template_name, {'form': form, 'result': result})


class EntryDetailView(DetailView):
    model = BlogEntry
    context_object_name = 'entry'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class EntryListView(ListView):
    model = BlogEntry
    paginate_by = 3
    context_object_name = 'blog_entries'


class EntryUpdateView(PermissionRequiredMixin, UpdateView):
    model = BlogEntry
    form_class = EntryForm
    template_name = 'blog/update_blog_entry.html'
    permission_required = "blog.change_blogentry"

    def form_valid(self, form):
        if form.is_valid():
            saved_form = form.save()
            saved_form.entry_slug = slugify(
                saved_form.entry_title)
            saved_form.save()
            EntryUpdateView.success_url = f'{reverse_lazy("list_entry")}{saved_form.pk}'
        return super().form_valid(form)


class EntryDeleteView(PermissionRequiredMixin, DeleteView):
    model = BlogEntry
    success_url = reverse_lazy("list_entry")
    context_object_name = 'entry'
    permission_required = "blog.delete_blogentry"

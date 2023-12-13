from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('add_entry/', views.EntryCreateView.as_view(), name='add_entry'),
    path('list_entry/', cache_page(60)(views.EntryListView.as_view()), name='list_entry'),
    path('list_entry/<int:pk>', views.EntryDetailView.as_view(), name='entry_details'),
    path('list_entry/<int:pk>/delete',
         views.EntryDeleteView.as_view(), name='delete_entry'),
    path('list_entry/<int:pk>/update',
         views.EntryUpdateView.as_view(), name='update_entry'),
]

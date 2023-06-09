from django.urls import path
from contacts.views import contact_list, add_contact, edit_contact, delete_contact, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('contact_list/', contact_list, name='contact_list'),
    path('add_contact/', add_contact, name='add_contact'),
    path('edit_contact/<int:contact_id>/', edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', delete_contact, name='delete_contact'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



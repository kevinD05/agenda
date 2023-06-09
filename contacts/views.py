from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .models import Contact
from django.http import HttpResponse

def homePageView(request):
    return HttpResponse("Hola, Fly!")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('contact_list')
    else:
        form = AuthenticationForm()
    return render(request, 'contacts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

from django.db import IntegrityError

from django.contrib import messages

def add_contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        
        if not first_name or not last_name or not email or not phone_number:
            error_message = 'Por favor, completa todos los campos obligatorios.'
            return render(request, 'contacts/add_contact.html', {'error_message': error_message})
        
        if len(phone_number) > 8:
            error_message = 'El número de teléfono debe tener como máximo 8 dígitos.'
            return render(request, 'contacts/add_contact.html', {'error_message': error_message})
        
        # Verificar si ya existe un contacto con el mismo nombre y número de teléfono
        if Contact.objects.filter(first_name=first_name, phone_number=phone_number).exists():
            error_message = 'Ya existe un contacto con el mismo nombre y número de teléfono.'
            messages.error(request, error_message)
            return render(request, 'contacts/add_contact.html')
        
        Contact.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        messages.success(request, 'El contacto se ha agregado exitosamente.')
        return redirect('contact_list')
    
    return render(request, 'contacts/add_contact.html')
    
def edit_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    if request.method == 'POST':
        contact.first_name = request.POST['first_name']
        contact.last_name = request.POST['last_name']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone_number']
        contact.save()
        return redirect('contact_list')
    return render(request, 'contacts/edit_contact.html', {'contact': contact})

def delete_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    
    if request.method == 'POST':
        # Eliminar el contacto de la base de datos
        contact.delete()
        return redirect('contact_list')
    
    return render(request, 'contacts/delete_contact.html', {'contact': contact, 'warning_message': '¿Estás seguro de que deseas eliminar este contacto?'})

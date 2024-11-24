from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import UserRegister, RegisterForm, LoginForm
from .models import Register
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

def jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def registration(request):
    if request.method == 'POST':
        user_form = UserRegister(request.POST)
        register_form = RegisterForm(request.POST)
        
        if user_form.is_valid() and register_form.is_valid():
            user = user_form.save(commit=True)
            register_user = register_form.save(commit=False)
            register_user.user = user
            register_user.save()
            token = jwt_token(user)
            
            user_token_data = {
                'id': user.id,
                'username': register_user.fio,
                'email': user.email,
            }
            
            register_token = {
                'id': register_user.id,
                'fio': register_user.fio,
                'university_group': register_user.university_group
            }
            
            forms_data = {
                'user_check': {
                    'is_valid': True,
                    'errors': None,
                    'cleaned_data': user_token_data
                },
                'register_check': {
                    'is_valid': True,
                    'errors': None,
                    'cleaned_data': register_token
                },
                'token': token
            }
            
            return JsonResponse(forms_data)
        else:
            errors = {
                'user_form_errors': user_form.errors.as_json(),
            }
            return JsonResponse(errors, status=400)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# def registration(request):
#     if request.method == 'POST':
#         user_form = UserRegister(request.POST)
#         register_form = RegisterForm(request.POST)
#         if user_form.is_valid() and register_form.is_valid():
#             user = user_form.save(commit=True)
#             register_user = register_form.save(commit=False)
#             register_user.user = user
#             register_user.save()
            
        
#     user_form = UserRegister()
#     register_form = RegisterForm()
    
#     context = {
#         'user_form': user_form,
#         'register_form': register_form,
#     }
    
#     return render(request, 'register/register.html', context)

@csrf_exempt
def login_jwt(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                user.last_login = now()
                user.save()
                
            if user is not None:
                token = jwt_token(user)
                
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff
                }
                
                response_data = {
                    'user': user_data,
                    'token': token
                }
                
                return JsonResponse(response_data)
            else:
                return JsonResponse(
                    {
                        'errors': 'Invalid credentials'
                    }, status=401
                )
        else:
            return JsonResponse({'errors': login_form.errors.as_json()}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def logout_jwt(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'you succesfully logout'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
                

@login_required
def my_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'status': 'logged_in'})
    else:
        return JsonResponse({'status': 'not_logged_in'}, status=401)


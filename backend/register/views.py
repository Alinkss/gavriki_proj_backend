from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import UserRegister, RegisterForm, LoginForm, JwtForm, RegisterTeacherForm
from .models import Register, RegisterForTeacher
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import logging
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model

# def user(request, user_id):
#     user = User.objects.get(id=user_id)

#     context = {
#         'user': {
#             'id': user.id,
#             'username': user.username
#         },
#     }

#     return JsonResponse(context)

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
def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        user = get_user_model().objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        return None
    except get_user_model().DoesNotExist:
        logger.error("User does not exist")
        return None

@csrf_exempt
def get_user_by_jwt(request):
    if request.method == 'POST':
        form = JwtForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            user = decode_jwt(token)
            if user:
                user_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }
                return JsonResponse({'user': user_data})
            else:
                return JsonResponse({'error': 'Invalid token'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# def login_jwt(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']
            
#             user = User.objects.get(username=username, password=password)
            
#             if user is not None:
#                 user.last_login = now()
#                 user.save()

#                 token = jwt_token(user)
                
#                 context = {
#                     'user': user,
#                     'token': token,
#                     'success': True,
#                 }
#                 return render(request, 'register/login_success.html', context)
#             else:
#                 return render(request, 'register/login.html', {
#                     'form': login_form,
#                     'errors': ['Invalid credentials'],
#                 })
#         else:
#             return render(request, 'register/login.html', {
#                 'form': login_form,
#                 'errors': login_form.errors,
#             })
#     else:
#         login_form = LoginForm()
#         return render(request, 'register/login.html', {'form': login_form})
    
def login_jwt(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = User.objects.get(username=username, password=password)
            
            if user is not None:
                user.last_login = now()
                user.save()
                
            print(f"Authenticated user: {user}")
            
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

def login_for_teacher(request):
    if request.method == 'POST':
        login_form = RegisterTeacherForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            
            user = RegisterForTeacher.objects.get(username=username, password=password)
            if user is not None:
                user.last_login = now()
                user.save()
            
            print(f"Authenticated teacher: {user}")
            
            if user is not None:
                token = jwt_token(user)
                
                user_data = {
                    'id': user.id,
                    'fio': user.fio,
                    'username': user.username
                }
                
                response = {
                    'user_data': user_data,
                    'token': token
                }
                
                return JsonResponse(response)
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


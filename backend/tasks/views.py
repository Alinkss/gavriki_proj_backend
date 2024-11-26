from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task, StudentSendTask
from django.contrib.auth.decorators import login_required
from tasks.forms import SendTaskForm
from django.http import JsonResponse
from register.models import RegisterForTeacher, Register

def task_detail(request, task_id=None):
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    
    is_teacher = RegisterForTeacher.objects.filter(username=user.username).exists()
    is_student = Register.objects.filter(user=user).exists()
    
    if not is_teacher and not is_student:
        return JsonResponse({'error': 'Access denied.'}, status=403)

    if request.method == 'POST' and is_student:
        send_form = SendTaskForm(request.POST)
        if send_form.is_valid():
            send = send_form.save(commit=False)
            send.user = request.user
            send.task = task
            send.save()
            
            return redirect('task_detail', task_id=task.id)
    else:
        send_form = SendTaskForm()
        
    if is_teacher:
        submissions = StudentSendTask.objects.filter(task=task).order_by('-published_date')
    elif is_student:
        submissions = StudentSendTask.objects.filter(task=task, user=user).order_by('-published_date')
    else:
        return JsonResponse({'error': 'Access denied.'}, status=403)
    
    submissions = SendTaskForm.objects.filter(task=task)
    stud_has_send = submissions.exists()
    
    response_data = {
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
        },
        'submissions': [
            {
                'id': submission.id,
                'user': submission.user.username,
                'published_date': submission.published_date.strftime('%Y-%m-%d %H:%M'),
            }
            for submission in submissions
        ],
        'stud_has_send': stud_has_send,
        'is_teacher': is_teacher,
        'is_student': is_student,
    }
    
    return JsonResponse(response_data)

# def task_detail(request, task_id=None):
#     task = get_object_or_404(Task, id=task_id)
#     user = request.user

#     is_teacher = RegisterForTeacher.objects.filter(username=user.username).exists()
#     is_student = Register.objects.filter(user=user).exists()

#     if not is_teacher and not is_student:
#         return render(request, 'tasks/access_denied.html', {'error': 'Access denied.'})

#     if request.method == 'POST' and is_student:
#         send_form = SendTaskForm(request.POST, request.FILES)
#         if send_form.is_valid():
#             send = send_form.save(commit=False)
#             send.user = user
#             send.task = task
#             send.save()
#             return redirect('task_detail', task_id=task.id)
#     else:
#         send_form = SendTaskForm()

#     if is_teacher:
#         submissions = StudentSendTask.objects.filter(task=task).order_by('-published_date')
#     elif is_student:
#         submissions = StudentSendTask.objects.filter(task=task, user=user).order_by('-published_date')
#     else:
#         submissions = []

#     stud_has_send = submissions.exists()

#     context = {
#         'task': task,
#         'form': send_form,
#         'submissions': submissions,
#         'stud_has_send': stud_has_send,
#         'is_teacher': is_teacher,
#         'is_student': is_student,
#     }

#     return render(request, 'tasks/task_detail.html', context)

# def task_detail(request, task_id=None):
#     task = get_object_or_404(Task, id=task_id)
#     context = {
#         'task': {
#             'id': task.id,
#             'title': task.title,
#             'content': task.content,
#             'dedline': task.dedline,
#             'published_date': task.published_date,
#         }
#     }
#     return JsonResponse(context)
            
            
# def list_tasks(request):
#     tasks = Task.objects.all()
#     task_list = [
#         {
#             'id': task.id,
#             'title': task.title,
#             'content': task.content,
#             'dedline': task.dedline.strftime('%Y-%m-%d %H:%M:%S'),
#             'published_date': task.published_date.strftime('%Y-%m-%d %H:%M:%S') if task.published_date else None,
#             'teacher_fio': f"{task.teacher.fio}" if task.teacher else None
#         }
#         for task in tasks
#     ]
    
#     context = {
#         'tasks': task_list
#     }
    
#     return JsonResponse(context)

def list_tasks(request):
    task = Task.objects.all()
    return render(request, 'tasks/list_tasks.html', {'tasks': task})
    
    
    
# @login_required
# def send_task(request, task_id):
#     tasks = get_object_or_404(Task, id=task_id)
#     if request.method == 'POST':
#         send_form = SendTaskForm(request.POST)
#         if send_form.is_valid():
#             send = send_form.save(commit=False)
#             send.user = request.user
#             send.task = tasks
#             send.save()
            
#             return redirect('task_detail', task_id=tasks.id)
#     else:
#         send_form = SendTaskForm()
        
#     submissions = SendTaskForm.objects.filter(task=tasks)
    
#     context = {
#         'form': send_form,
#         'task': tasks,
#         'submissions': submissions,
#     }
    
#     return render(request, 'tasks/task_detail.html', context)

@login_required
def send_task(request, task_id):
    tasks = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        send_form = SendTaskForm(request.POST)
        if send_form.is_valid():
            send = send_form.save(commit=False)
            send.user = request.user
            send.task = tasks
            send.save()
            
            response_data = {
                'success': 'success',
                'id': tasks.id,
                'user': request.user.username,
                'title': tasks.title,
                'submission_id': send.id,
            }    
            
            return JsonResponse(response_data)
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is invalid.'}, status=400)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)
        
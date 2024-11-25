from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from tasks.forms import SendTaskForm
from django.http import JsonResponse

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
            
            return redirect('task_detail', task_id=tasks.id)
    else:
        send_form = SendTaskForm()
        
    submissions = SendTaskForm.objects.filter(task=tasks)
    
    context = {
        'form': send_form,
        'task': tasks,
        'submissions': submissions,
    }
    
    return render(request, 'tasks/task_detail.html', context)
    
# def task_detail(request, task_id=None):
#     task = get_object_or_404(Task, id=task_id)
#     context = {
#         'task': task
#     }
#     return render(request, 'tasks/task_detail.html', context)


def task_detail(request, task_id=None):
    task = get_object_or_404(Task, id=task_id)
    context = {
        'task': {
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'dedline': task.dedline,
            'published_date': task.published_date,
        }
    }
    return JsonResponse(context)
            
            
def list_tasks(request):
    tasks = Task.objects.all()
    task_list = [
        {
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'dedline': task.dedline.strftime('%Y-%m-%d %H:%M:%S'),
            'published_date': task.published_date.strftime('%Y-%m-%d %H:%M:%S') if task.published_date else None,
        }
        for task in tasks
    ]
    
    context = {
        'tasks': task_list
    }
    
    return JsonResponse(context)

# def list_tasks(request):
#     task = Task.objects.all()
#     return render(request, 'tasks/list_tasks.html', {'tasks': task})
    
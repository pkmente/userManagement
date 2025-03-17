from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from .tasks import send_task_email
# from django.conf import settings
import csv
from django.http import HttpResponse

#------------------For creating the new tasks--------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_task(request):
    request.data['user'] = request.user.id
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        task = serializer.save(user=request.user)

        # Send an email after creating the new task
        subject = "New Task Created"
        message = f"Hello {request.user.username},\n\nYou have successfully created a new task:\n\nTitle: {task.title}\nDescription: {task.description}\nStatus: {task.status}\nAssignee: {task.assignee}\nPriority: {task.priority}\n\nThank you!"
        recipient_list = [request.user.email]  # Sending to the task creator's email

        # send_mail(
        #     subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False
        # )
        send_task_email.delay(subject, message, recipient_list)  # Celery task


        # Update cache after creating a new task
        cache_key = f"tasks_{request.user.id}"
        tasks = Task.objects.filter(user=request.user)
        cache.set(cache_key, TaskSerializer(tasks, many=True).data, timeout=60)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------




# ---------For to show the list of tasks for the respective user------------------------------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_tasks(request):
    cache_key = f"tasks_{request.user.id}"
    tasks = cache.get(cache_key)

    if tasks is not None:
        print("Data fetched from cache")
        return Response(tasks)  #Return task cached data

 
    tasks = Task.objects.filter(user=request.user)
    # print("=========tasks=at list tasks=====",list(tasks['tasks']))
    serializer = TaskSerializer(tasks, many=True)

    cache.set(cache_key, serializer.data, timeout=60*5)
    tasks_data = serializer.data
    print("tasks_data-------",tasks_data)
    return Response(serializer.data)
# -------------------------------------------------------------------




# -----------------------------For tasks filteration using due date--------------------------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def filt_list_tasks(request):
    cache_key = f"tasks_{request.user.id}"
    tasks = cache.get(cache_key)

    if tasks is not None:
        print("Data fetched from cache")
        return Response(tasks) #Tasks from cache

 
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    serializer = TaskSerializer(tasks, many=True)

    # Store in cache for next requests
    cache.set(cache_key, serializer.data, timeout=60*5)

    return Response(serializer.data)
# -------------------------------------------------------------------




# -----For Updating the task details like assignee, status of the task etc..-------------------

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        #Sending an email after updating the task
        subject = "Task - updated"
        message = f"Hello {request.user.username},\n\nYou have successfully Updated task:\n\nTitle: {task.title}\nDescription: {task.status}\nDue Date: {task.due_date}\nAssignee: {task.assignee}\n\nThank you!"
        recipient_list = [request.user.email]  # Sending email to the task creator's email


        # send_mail(
        #     subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False
        # )
        send_task_email.delay(subject, message, recipient_list)  # Email task with celery module

        cache_key = f"tasks_{request.user.id}"
        tasks = Task.objects.filter(user=request.user)
        cache.set(cache_key, TaskSerializer(tasks, many=True).data, timeout=60*5)

        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-------------------------------------------------------------------------------------



#--------------For deleting the task------------------------

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        # 🔹 Send an email after creating the task
        subject = "Task - Deleted"
        message = f"Hello {request.user.username},\n\nYou have successfully deleted task with:\n\nTitle: {task.title}\nDescription: {task.status}\nDue Date: {task.due_date}\n\n\nThank you!"
        # recipient_list = [request.user.email]  # Sending to the task creator's email
        recipient_list = [request.user.email]  # Sending to the task creator's email


        # send_mail(
        #     subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False
        # )
        send_task_email.delay(subject, message, recipient_list)  

        cache_key = f"tasks_{request.user.id}"
        tasks = Task.objects.filter(user=request.user)
        cache.set(cache_key, TaskSerializer(tasks, many=True).data, timeout=60*5)

        return Response({"success": "Task successfully deleted"}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
#---------------------------------------------------------------------------------------

#-------------------For CSV file exporting - list of tasks---------------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_tasks_to_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Description', 'Priority', 'Due Date', 'Status', 'Assignee', 'User'])

    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        writer.writerow([
            task.id, task.title, task.description, task.priority, 
            task.due_date, task.status, task.assignee.id, task.user.id
        ])

    return response
#-------------------------------------------------------------------------------

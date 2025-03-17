from django.urls import path
from .views import create_task, list_tasks, filt_list_tasks, update_task, delete_task

urlpatterns = [
    path('tasks/', list_tasks, name='list_tasks'),
    path('tasks/filt', filt_list_tasks, name='filt_list_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
     
]

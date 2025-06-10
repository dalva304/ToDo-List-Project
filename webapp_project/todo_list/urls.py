from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteTask

urlpatterns = [
    path('tasks/', views.TaskList.as_view(), name='tasks'),  # Changed from empty string to 'tasks/'
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('task-create/', views.TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', views.DeleteTask.as_view(), name='task-delete'),
    path('task-update-status/<int:pk>/', views.update_task_status, name='task-update-status'),
    path('create-task-group/', views.create_task_group, name='create-task-group'),
    path('rename-task-group/', views.rename_task_group, name='rename-task-group'),
    path('delete-task-group/', views.delete_task_group, name='delete-task-group'),
    path('add-tasks-to-group/', views.add_tasks_to_group, name='add-tasks-to-group'),
    path('remove-task-from-group/', views.remove_task_from_group, name='remove-task-from-group'),
    path('', views.redirect_to_tasks, name='home'),
]
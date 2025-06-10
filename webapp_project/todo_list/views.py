from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from .models import Task,TaskGroup
from .forms import UserRegisterForm, TaskUserForm, TaskAdminForm
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('login')
def redirect_to_tasks(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    else:
        return redirect('login')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'todo_list/register.html', {'form': form})

# In views.py - TaskList view
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo_list/task_list.html' 
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            #admin view
            user_filter = self.request.GET.get('user_filter', '')
            if user_filter:
                tasks = Task.objects.filter(user_id=user_filter)
            else:
                tasks = Task.objects.all()
        else:
            # reg users view
            tasks = Task.objects.filter(user=self.request.user)
        
        # Use a timezone-aware datetime.max replacement
        max_date = timezone.make_aware(datetime.max.replace(year=9999, month=12, day=31))
        
        # order tasks by completion
        return sorted(tasks, key=lambda t: (1 if t.status == 'completed' else 0, t.duedate or max_date))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['users'] = User.objects.all()
        
        # Add task groups to context
        context['task_groups'] = TaskGroup.objects.filter(user=self.request.user)
        
        if 'task_completed' in self.request.session:
            context['task_completed'] = self.request.session['task_completed']
            del self.request.session['task_completed']
            self.request.session.modified = True
        
        return context
        
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo_list/task.html'
    
    def get_queryset(self):
        # Superusers can view any task, regular users only their own
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(user=self.request.user)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('tasks')
    
    def get_form_class(self):
        # Superusers can select which user to assign the task to
        if self.request.user.is_superuser:
            return TaskAdminForm  # We'll create this form
        else:
            return TaskUserForm  # We'll create this form too
    
    def form_valid(self, form):
        # If not a superuser, automatically assign the task to the current user
        if not self.request.user.is_superuser:
            form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy('tasks')
    
    def get_form_class(self):
        if self.request.user.is_superuser:
            return TaskAdminForm
        else:
            return TaskUserForm
    
    def get_queryset(self):
        # Superusers can edit any task, regular users only their own
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(user=self.request.user)

def update_task_status(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            task = Task.objects.get(pk=pk)
            
            # Check if user is allowed to update this task
            if request.user.is_superuser or task.user == request.user:
                old_status = task.status
                new_status = request.POST.get('status')
                
                print(f"Update task status: Task {pk}, Old status: {old_status}, New status: {new_status}")
                print(f"POST data: {request.POST}")
                
                # Handle the case for custom status
                if new_status == 'custom':
                    custom_status = request.POST.get('custom_status', '').strip()
                    is_new_custom = request.POST.get('is_new_custom') == '1'
                    
                    print(f"Custom status: '{custom_status}', Is new: {is_new_custom}")
                    
                    if custom_status:
                        task.status = 'custom'
                        task.custom_status = custom_status
                        print(f"Setting custom status to: {custom_status}")
                    else:
                        # If no custom status provided, don't change anything
                        print("No custom status provided, not changing")
                        return HttpResponseRedirect(reverse('tasks'))
                else:
                    # Regular status update
                    task.status = new_status
                    if new_status != 'custom':
                        task.custom_status = ''
                
                # Check if this is a transition to completed
                if old_status != 'completed' and new_status == 'completed':
                    request.session['task_completed'] = task.id
                        
                task.save()
                print(f"Task saved with status: {task.status}, custom status: '{task.custom_status}'")
                
        except Task.DoesNotExist:
            print(f"Task {pk} does not exist")
            
    return HttpResponseRedirect(reverse('tasks'))

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
    def get_queryset(self):
        # Superusers can delete any task, regular users only their own
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(user=self.request.user)
        
# TASK GROUPS VIEWS 
#creating tasks !! 
def create_task_group(request):
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST.get('name')
        color = request.POST.get('color', 'primary')  # Default to primary if not specified
        if name:
            group = TaskGroup.objects.create(user=request.user, name=name, color=color)
            group.save()
    return HttpResponseRedirect(reverse('tasks'))
#renaming /editing task group !
def rename_task_group(request):
    if request.method == 'POST' and request.user.is_authenticated:
        group_id = request.POST.get('group_id')
        name = request.POST.get('name')
        if group_id and name:
            try:
                group = TaskGroup.objects.get(id=group_id, user=request.user)
                group.name = name
                group.save()
            except TaskGroup.DoesNotExist:
                pass
    return HttpResponseRedirect(reverse('tasks'))
#deleting task group(whole) !!
def delete_task_group(request):
    if request.method == 'POST' and request.user.is_authenticated:
        group_id = request.POST.get('group_id')
        if group_id:
            try:
                group = TaskGroup.objects.get(id=group_id, user=request.user)
                group.delete()
            except TaskGroup.DoesNotExist:
                pass
    return HttpResponseRedirect(reverse('tasks'))
#adding tasks to group !!
def add_tasks_to_group(request):
    print("Entered add_tasks_to_group view")
    if request.method == 'POST' and request.user.is_authenticated:
        print("POST request with authenticated user")
        print("POST data:", request.POST)
        
        group_id = request.POST.get('group_id')
        task_ids = request.POST.getlist('task_ids')
        
        print(f"Group ID: {group_id}")
        print(f"Task IDs: {task_ids}")
        
        if group_id and task_ids:
            try:
                group = TaskGroup.objects.get(id=group_id, user=request.user)
                print(f"Found group: {group}")
                for task_id in task_ids:
                    try:
                        task = Task.objects.get(id=task_id)
                        print(f"Found task: {task}")
                        # Check if user is allowed to access this task
                        if request.user.is_superuser or task.user == request.user:
                            group.tasks.add(task)
                            print(f"Added task {task_id} to group")
                        else:
                            print(f"User not authorized for task {task_id}")
                    except Task.DoesNotExist:
                        print(f"Task {task_id} does not exist")
            except TaskGroup.DoesNotExist:
                print(f"Group {group_id} does not exist")
        else:
            print("Missing group_id or task_ids")
    else:
        print("Not a POST request or user not authenticated")
            
    return HttpResponseRedirect(reverse('tasks'))
#removing a task from the group !
def remove_task_from_group(request):
    if request.method == 'POST' and request.user.is_authenticated:
        group_id = request.POST.get('group_id')
        task_id = request.POST.get('task_id')
        if group_id and task_id:
            try:
                group = TaskGroup.objects.get(id=group_id, user=request.user)
                task = Task.objects.get(id=task_id)
                group.tasks.remove(task)
            except (TaskGroup.DoesNotExist, Task.DoesNotExist):
                pass
    return HttpResponseRedirect(reverse('tasks'))

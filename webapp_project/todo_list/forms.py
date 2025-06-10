# todo_list/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TaskUserForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'custom_status', 'duedate']
        widgets = {
            'duedate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make custom_status conditionally required
        self.fields['custom_status'].required = False
        
        # Add JavaScript to show/hide custom_status field based on status selection
        self.fields['status'].widget.attrs.update({
            'class': 'form-select status-select',
            'onchange': 'toggleCustomStatus(this.value)'
        })

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'custom_status', 'duedate', 'user']
        widgets = {
            'duedate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Improve the user field display
        self.fields['user'].queryset = User.objects.all()
        self.fields['user'].label_from_instance = lambda obj: f"{obj.username} ({obj.email if obj.email else 'No email'})"
        
        # Make custom_status conditionally required
        self.fields['custom_status'].required = False
        
        # Add JavaScript to show/hide custom_status field based on status selection
        self.fields['status'].widget.attrs.update({
            'class': 'form-select status-select',
            'onchange': 'toggleCustomStatus(this.value)'
        })
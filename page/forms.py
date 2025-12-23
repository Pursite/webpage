from django import forms
from .models import Athnticate

class AthnticateForm(forms.ModelForm):
    class Meta:
        model = Athnticate
        fields = ['name', 'phone_number', 'email', 'message']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+98...',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
            }),
            'message': forms.Textarea(attrs={  
                'placeholder': 'Write your message here...',
                'rows': 5,
            }),
        }





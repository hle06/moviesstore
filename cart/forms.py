from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'statement']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your name (optional)'
                }
            ),
            'statement': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'How was your checkout experience?',
                    'rows': 4
                }
            ),
        }
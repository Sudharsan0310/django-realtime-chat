from django import forms
from .models import ChatGroup, GroupMessage

class ChatmessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Type your message...',
                'class': 'flex-1 p-3 rounded-lg bg-gray-700 text-white',
                'maxlength': 300,
                'autocomplete': 'off'
            })
        }


class GroupChatCreateForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name', 'description', 'group_icon']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Enter group name...',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter group description...',
                'rows': 4,
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'group_icon': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            })
        }
        labels = {
            'groupchat_name': 'Group Name',
            'description': 'Description',
            'group_icon': 'Group Icon'
        }


class GroupChatEditForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name', 'description', 'group_icon']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Enter group name...',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter group description...',
                'rows': 4,
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'group_icon': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            })
        }
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import shortuuid

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    group_icon = models.ImageField(upload_to='group_icons/', null=True, blank=True)
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.groupchat_name or self.group_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.group_icon:
            img = Image.open(self.group_icon.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.group_icon.path)
    
    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def online_count(self):
        return self.users_online.count()
    
    @property
    def is_dm(self):
        return self.is_private and self.members.count() == 2
    
    def get_other_user(self, current_user):
        if self.is_dm:
            return self.members.exclude(id=current_user.id).first()
        return None


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'

    class Meta:
        ordering = ['-created']


class UserOnlineStatus(models.Model):
    """Track which user is in which chatroom"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='online_status')
    current_chatroom = models.ForeignKey(ChatGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='active_users')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Online Status"
        verbose_name_plural = "User Online Statuses"
    
    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"
    
    @property
    def time_since_last_seen(self):
        """Get human-readable time since last seen"""
        if self.is_online:
            return "Online now"
        
        delta = timezone.now() - self.last_seen
        
        if delta.seconds < 60:
            return "Just now"
        elif delta.seconds < 3600:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        elif delta.seconds < 86400:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        else:
            days = delta.days
            return f"{days}d ago"
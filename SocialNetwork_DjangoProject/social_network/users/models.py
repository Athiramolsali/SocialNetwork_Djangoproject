from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='user_sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='user_received_requests', on_delete=models.CASCADE)
    time  = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class roomModel(models.Model):
    creator  = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True)
    roomName = models.CharField(max_length=50)
    created  = models.DateTimeField(auto_now_add=True)
    timeout  = models.IntegerField(default=0)

class message(models.Model):
    content = models.CharField(max_length = 240)
    author  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sent    = models.DateTimeField(auto_now_add=True)
    room    = models.ForeignKey(roomModel, on_delete=models.CASCADE)
    

class ChatLogMessage(models.Model):
    room    = models.ForeignKey(roomModel, on_delete=models.CASCADE, null=True)
    sender  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=250, null=True)
    content = models.CharField(max_length = 240)
    time    = models.DateTimeField(auto_now_add=True)
    @classmethod
    def create(self, room, sender, username, content):
        message = self(room=room, sender=sender,username=username, content=content)
        return message

class chatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(roomModel, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=250, null=True)


class Follower(models.Model):
    following = models.ForeignKey(User, related_name = 'following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name = 'followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')
    
    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)
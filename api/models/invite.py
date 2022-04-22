from django.db import models
# we're going to be using a special method to find our user model
from django.contrib.auth import get_user_model
# we dont want to directly import our user model, we want to use this method instead.

# Create models here.
class Invite(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  title = models.CharField(max_length=100)
  date = models.DateField()
  time = models.TimeField(max_length=100)
  location = models.CharField(max_length=100)
  details = models.CharField(max_length=100)
  accepted = models.BooleanField(default=False)
  # For user ownership, we'll add a new field 'host_id' which keeps track
  # of the user id who owns this invite and a second FK for the 
  # friend profile (the recipient of the invite)
  host_id = models.ForeignKey(
      get_user_model(),
      related_name='user_host_id',
      on_delete=models.CASCADE
  )
  friend_id = models.ForeignKey(
      get_user_model(),
      related_name='user_friend_id',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The invite '{self.title}' is on {self.date} at {self.time} . It is located at {self.location} here are the details {self.details}."

  def as_dict(self):
    """Returns dictionary version of Invite models"""
    return {
        'id': self.id,
        'title': self.title,
        'date': self.date,
        'time': self.time,
        'location': self.location,
        'details': self.details,
        'accepted': self.accepted,
        'host_id': self.host_id,
        'friend_id': self.friend_id
    }

from django.db import models
# we're going to be using a special method to find our user model
from django.contrib.auth import get_user_model
# we dont want to directly import our user model, we want to use this method instead.

# Create your models here.
class Profile(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  about_me = models.CharField(max_length=1000)
  # For user ownership, we'll add a new field 'owner' which keeps track
  # of the user id who owns this the mango
  user_id = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The profile named '{self.name}' is {self.age} years old. About them: {self.about_me} ."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'about_me': self.about_me,
        'user': self.user_id
    }
from django.db import models
from django.contrib.auth.models import AbstractUser
from mytools.resetpasstoken import reset_token


class User(AbstractUser):
    email = models.EmailField(unique=True , null=False)
    balance = models.BigIntegerField(default=0, null=True)
    image = models.ImageField(blank=True, default='profiles/defult_prof.jpg', upload_to='profiles/')
    special_til = models.DateTimeField(null=True)
    reset_pass_token = models.CharField(null=False , max_length=20)

    def save(self, *args, **kwargs):
        if self.reset_pass_token:
            super(User, self).save(*args, **kwargs)
        else:
            self.reset_pass_token = reset_token()
            super(User, self).save(*args, **kwargs)

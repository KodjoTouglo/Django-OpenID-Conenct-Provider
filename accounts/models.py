from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    )
    first_name = models.CharField("Name", max_length=30, blank=True, null=True)
    last_name = models.CharField("Surname", max_length=30, blank=True, null=True)
    email = models.EmailField("Email address", unique=True, blank=True, null=True)
    taxpayer_id = models.CharField("Taxpayer's identification number", max_length=32, blank=True, null=True)
    gender = models.CharField("Gender", choices=GENDER, max_length=10, blank=True, null=True)
    place_of_birth = models.CharField("Place of birth", max_length=40, blank=True, null=True)
    birth_date = models.DateField("Birthdate", null=True, blank=True)
    origin = models.CharField("From which country this users come from", max_length=50, blank=True, null=True)
    is_active = models.BooleanField("Active", default=True)

    class Meta:
        ordering = ["username"]
        verbose_name_plural = "Users"

    @property
    def uid(self):
        return self.username.split('@')[0]

    def persistent_id(self, entityid):
        """
        returns persistent id related to a recipient (sp) entity id
        :param entityid:
        :return:
        """
        pid = PersistentId.objects.filter(user=self, recipient_id=entityid).last()
        if pid:
            return pid.persistent_id

    def get_oidc_birthdate(self):
        return self.birth_date.strftime('%Y-%m-%d') if self.birth_date else ''

    def get_oidc_lastlogin(self):
        return self.last_login.timestamp() if self.last_login else ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class PersistentId(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    persistent_id = models.CharField("Persistent Stored ID", max_length=254, blank=True, null=True)
    recipient_id = models.CharField("Relying-Party entityID", max_length=254, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Persistent Id"
        verbose_name_plural = "Persistent Id"

    def __str__(self):
        return '{}: {} to {} [{}]'.format(self.user,
                                          self.persistent_id,
                                          self.recipient_id,
                                          self.created)


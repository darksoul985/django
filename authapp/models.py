from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        verbose_name='Аватарка',
        upload_to='user',
        blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name='Возраст',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный пльзователь'
    )
    activation_key = models.CharField(
        max_length=128,
        blank=True
    )
    activation_key_expires = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    def is_activation_key_expired(self):
        """ checking the activation pass by mail """
        now_date = now() - timedelta(hours=48)
        if now_date <= self.activation_key_expires:
            return False
        return True


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOISES = (

        (MALE, 'M'),
        (FEMALE, 'W')
    )

    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )
    tagline = models.CharField(
        verbose_name='тэги',
        max_length=128,
        blank=True
    )
    about_me = models.TextField(
        verbose_name='о себе',
        max_length=512,
        blank=True
    )
    gender = models.CharField(
        verbose_name='пол',
        max_length=1,
        choices=GENDER_CHOISES,
        blank=True
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()

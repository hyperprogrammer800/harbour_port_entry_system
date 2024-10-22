# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Person
# import logging

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         logger.info(f'Creating profile for {instance.username}')
#         print("KWARGS---->",instance)
#         Person.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     logger.info(f'Saving profile for {instance.username}')
#     instance.person.save()
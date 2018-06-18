from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserData(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    city = models.CharField(max_length=30, default=None)
    contact = models.CharField(max_length=15, default=None)
    dateOfBirth = models.DateField(default=None)
    photo = models.ImageField(upload_to='home/pic_folder/', default='no-img.jpg')


class Pet(models.Model):
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30, default=None)
    weight = models.FloatField(default=None, null=True)
    height = models.FloatField(default=None, null=True)
    type = models.CharField(max_length=30, default=None)
    other = models.CharField(max_length=30, default=None, null=True)
    breed = models.CharField(max_length=30, default=None, null=True)
    age = models.IntegerField(default=None)
    photo = models.ImageField(upload_to='home/pic_folder/pets/', default='no-animal-img.png')


class StayRequest(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE, default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)


class StayPossibility(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    petType = models.CharField(default=None, max_length=10)


class Stay(models.Model):
    owner = models.ForeignKey(User, related_name="Owner", on_delete=models.SET_NULL, default=None, null=True)
    caretaker = models.ForeignKey(User, related_name="Caretaker", on_delete=models.SET_NULL, default=None, null=True)
    pet = models.ForeignKey(Pet, related_name="Pet", on_delete=models.SET_NULL, default=None, null=True)
    possibility = models.ForeignKey(StayPossibility, related_name="Possibility", on_delete=models.SET_NULL, null=True)
    request = models.ForeignKey(StayRequest, related_name="Request", on_delete=models.SET_NULL, null=True)
    posAgree = models.BooleanField(default=False, null=False)
    reqAgree = models.BooleanField(default=False, null=False)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    ownerOpinion = models.CharField(max_length=250, default=None, null=True)
    ownerType = models.PositiveSmallIntegerField(default=None, null=True)
    caretakerOpinion = models.CharField(max_length=250, default=None, null=True)
    caretakerType = models.PositiveSmallIntegerField(default=None, null=True)


class Conversation(models.Model):
    userId1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User1", default=None)
    userId2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User2", default=None)


class Message(models.Model):
    conversationId = models.ForeignKey(Conversation, on_delete=models.CASCADE, default=None)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(default=None)
    content = models.CharField(max_length=250, default=None)

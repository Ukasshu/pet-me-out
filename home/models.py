from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserData(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    city = models.CharField(max_length=30, default=None)
    contact = models.CharField(max_length=15, default=None)
    dateOfBirth = models.DateField(default=None)


class Pet(models.Model):
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30, default=None)
    weight = models.FloatField(default=None)
    height = models.FloatField(default=None)
    type = models.CharField(max_length=30, default=None)
    breed = models.CharField(max_length=30, default=None)
    age = models.IntegerField(default=None)


class Stay(models.Model):
    ownerId = models.ForeignKey(User, related_name="Owner", on_delete=models.CASCADE, default=None)
    caretakerId = models.ForeignKey(User, related_name="Caretaker", on_delete=models.CASCADE, default=None)
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE, default=None)
    date = models.DateField(default=None)
    ownerOpinion = models.CharField(max_length=250, default=None)
    ownerOpinionType = models.CharField(max_length=1, default=None)
    caretakerOpinion = models.CharField(max_length=250, default=None)
    caretakerOpinionType = models.CharField(max_length=1, default=None)


class StayRequest(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    petId = models.ForeignKey(Pet, on_delete=models.CASCADE, default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)


class StayPossibility(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)


class Conversation(models.Model):
    userId1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User1", default=None)
    userId2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User2", default=None)


class Message(models.Model):
    conversationId = models.ForeignKey(Conversation, on_delete=models.CASCADE, default=None)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(default=None)
    content = models.CharField(max_length=250, default=None)

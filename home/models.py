from django.db import models


# Create your models here.

class User(models.Model):
    firstName: models.CharField(max_length=30)
    lastName: models.CharField(max_length=50)
    city: models.CharField(max_length=30)
    contact: models.CharField(max_length=15)
    mail: models.CharField(max_length=100)
    dateOfBirth: models.DateField


class Pet(models.Model):
    ownerId: models.ForeignKey(User, on_delete=models.CASCADE)
    name: models.CharField(max_length=30)
    weight: models.FloatField
    height: models.FloatField
    type: models.CharField(max_length=30)
    breed: models.CharField(max_length=30)
    age: models.IntegerField


class Stay(models.Model):
    ownerId: models.ForeignKey(User, related_name="Owner", on_delete=models.CASCADE)
    caretakerId: models.ForeignKey(User, related_name="Caretaker", on_delete=models.CASCADE)
    petId: models.ForeignKey(Pet, on_delete=models.CASCADE)
    date: models.DateField
    ownerOpinion: models.CharField(max_length=250)
    ownerOpinionType: models.CharField(max_length=1)
    caretakerOpinion: models.CharField(max_length=250)
    caretakerOpinionType: models.CharField(max_length=1)


class StayRequest(models.Model):
    userId: models.ForeignKey(User, on_delete=models.CASCADE)
    petId: models.ForeignKey(Pet, on_delete=models.CASCADE)
    startDate: models.DateField
    endDate: models.DateField


class StayPossibility(models.Model):
    userId: models.ForeignKey(User, on_delete=models.CASCADE)
    startDate: models.DateField
    endDate: models.DateField


class Conversation(models.Model):
    userId1: models.ForeignKey(User, on_delete=models.CASCADE, related_name="User1")
    userId2: models.ForeignKey(User, on_delete=models.CASCADE, related_name="User2")


class Message(models.Model):
    conversationId: models.ForeignKey(Conversation, on_delete=models.CASCADE)
    senderId: models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp: models.DateTimeField
    content: models.CharField(max_length=250)


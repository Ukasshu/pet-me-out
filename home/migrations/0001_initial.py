# Generated by Django 2.0.4 on 2018-06-18 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='User1', to=settings.AUTH_USER_MODEL)),
                ('userId2', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='User2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=None)),
                ('content', models.CharField(default=None, max_length=250)),
                ('conversationId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Conversation')),
                ('senderId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=30)),
                ('weight', models.FloatField(default=None, null=True)),
                ('height', models.FloatField(default=None, null=True)),
                ('type', models.CharField(default=None, max_length=30)),
                ('other', models.CharField(default=None, max_length=30, null=True)),
                ('breed', models.CharField(default=None, max_length=30, null=True)),
                ('age', models.IntegerField(default=None)),
                ('photo', models.ImageField(default='no-animal-img.png', upload_to='home/pic_folder/pets/')),
                ('ownerId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None)),
                ('ownerOpinion', models.CharField(default=None, max_length=250)),
                ('ownerOpinionType', models.CharField(default=None, max_length=1)),
                ('caretakerOpinion', models.CharField(default=None, max_length=250)),
                ('caretakerOpinionType', models.CharField(default=None, max_length=1)),
                ('caretakerId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Caretaker', to=settings.AUTH_USER_MODEL)),
                ('ownerId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Owner', to=settings.AUTH_USER_MODEL)),
                ('petId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='StayPossibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(default=None)),
                ('endDate', models.DateField(default=None)),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StayRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(default=None)),
                ('endDate', models.DateField(default=None)),
                ('petId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Pet')),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default=None, max_length=30)),
                ('contact', models.CharField(default=None, max_length=15)),
                ('dateOfBirth', models.DateField(default=None)),
                ('photo', models.ImageField(default='no-img.jpg', upload_to='home/pic_folder/')),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]

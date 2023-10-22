# Generated by Django 4.2.6 on 2023-10-22 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_studentmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('gender', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('cratedat', models.DateTimeField(auto_now_add=True)),
                ('updateat', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('courseid', models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.coursemodel')),
            ],
        ),
    ]
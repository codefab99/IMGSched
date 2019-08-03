# Generated by Django 2.2.2 on 2019-07-29 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('IMGSched', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.IntegerField(choices=[(1, 'Public'), (2, 'Private')]),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_level', models.IntegerField(choices=[(1, 'NORMAL USER'), (2, 'ADMIN')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('comment_text', models.TextField()),
                ('meeting_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting', to='IMGSched.Meeting')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time',),
            },
        ),
    ]
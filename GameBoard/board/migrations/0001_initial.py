# Generated by Django 5.0.2 on 2024-02-21 07:44

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_field', models.CharField(choices=[('tanks', 'Танки'), ('heals', 'Хилы'), ('DD', 'ДД'), ('merchants', 'Торговцы'), ('gildmasters', 'Гилдмастеры'), ('questgivers', 'Квестгиверы'), ('smiths', 'Кузнецы'), ('leatherworkers', 'Кожевники'), ('potioncookers', 'Зельевары'), ('spellmasters', 'Мастера заклинаний')], default='tanks', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('personal_email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.ad')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='board.user')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='board.user'),
        ),
    ]

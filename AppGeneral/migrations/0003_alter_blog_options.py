# Generated by Django 4.2.2 on 2023-07-13 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppGeneral', '0002_alter_blog_fecha'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-fecha']},
        ),
    ]
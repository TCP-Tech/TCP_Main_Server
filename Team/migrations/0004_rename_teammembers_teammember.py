# Generated by Django 4.2.4 on 2024-09-18 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0003_rename_member_teammembers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamMembers',
            new_name='TeamMember',
        ),
    ]

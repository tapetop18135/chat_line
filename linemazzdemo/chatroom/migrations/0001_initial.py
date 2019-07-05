# Generated by Django 2.2.3 on 2019-07-05 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('linemessageapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=1000, unique=True)),
                ('start_conversation_at', models.DateTimeField(auto_now_add=True)),
                ('end_conversation_at', models.DateTimeField(blank=True, null=True)),
                ('update_conversation_at', models.DateTimeField(auto_now=True)),
                ('line_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='linemessageapi.LineAccounts')),
                ('line_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='linemessageapi.LineContact')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(db_index=True, max_length=1000)),
                ('text', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, max_length=1000, null=True, upload_to='')),
                ('file', models.FileField(blank=True, max_length=1000, null=True, upload_to='')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_read', models.BooleanField(default=False)),
                ('raw_data', models.TextField(blank=True, null=True)),
                ('line_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='linemessageapi.LineAccounts')),
                ('line_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='linemessageapi.LineContact')),
            ],
        ),
    ]

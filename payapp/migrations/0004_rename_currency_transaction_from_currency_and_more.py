# Generated by Django 4.1.7 on 2023-03-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0003_alter_transaction_receiver_alter_transaction_sender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='currency',
            new_name='from_currency',
        ),
        migrations.AddField(
            model_name='transaction',
            name='to_currency',
            field=models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR')], default='USD', max_length=3),
            preserve_default=False,
        ),
    ]

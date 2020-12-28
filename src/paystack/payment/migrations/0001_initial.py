# Generated by Django 3.1.4 on 2020-12-28 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveBigIntegerField()),
                ('deducted_amount', models.PositiveBigIntegerField()),
                ('fully_deducted', models.BooleanField(default=False)),
                ('currency', models.CharField(blank=True, default='NGN', max_length=10, null=True)),
                ('channel', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(max_length=100)),
                ('refunded_by', models.EmailField(max_length=254)),
                ('refunded_at', models.DateTimeField()),
                ('expected_at', models.DateTimeField()),
                ('customer_note', models.TextField(blank=True, null=True)),
                ('merchant_note', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SplitSubAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subaccount_code', models.CharField(max_length=200)),
                ('business_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('primary_contact_name', models.CharField(blank=True, max_length=200, null=True)),
                ('primary_contact_email', models.CharField(blank=True, max_length=200, null=True)),
                ('primary_contact_phone', models.CharField(blank=True, max_length=13, null=True)),
                ('metadata', models.JSONField(blank=True, null=True)),
                ('settlement_bank', models.CharField(max_length=200)),
                ('account_number', models.IntegerField()),
                ('share', models.PositiveBigIntegerField(help_text='Percentage Share')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionSplit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('split_code', models.CharField(max_length=200)),
                ('integration', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=150, null=True)),
                ('currency', models.CharField(blank=True, default='NGN', max_length=10, null=True)),
                ('bearer_type', models.CharField(blank=True, max_length=100, null=True)),
                ('bearer_subaccount', models.CharField(blank=True, max_length=120, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subaccounts', models.ManyToManyField(through='payment.SplitSubAccount', to='payment.SubAccount')),
            ],
        ),
        migrations.AddField(
            model_name='splitsubaccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.subaccount'),
        ),
        migrations.AddField(
            model_name='splitsubaccount',
            name='split',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.transactionsplit'),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorization_code', models.CharField(blank=True, max_length=200, null=True)),
                ('card_type', models.CharField(blank=True, max_length=100, null=True)),
                ('last4', models.CharField(max_length=4, null=True)),
                ('exp_month', models.CharField(max_length=2, null=True)),
                ('exp_year', models.CharField(max_length=4, null=True)),
                ('bin', models.CharField(max_length=10, null=True)),
                ('bank', models.CharField(max_length=50, null=True)),
                ('brand', models.CharField(blank=True, max_length=10, null=True)),
                ('channel', models.CharField(blank=True, max_length=30, null=True)),
                ('signature', models.CharField(blank=True, max_length=200, null=True)),
                ('reusable', models.BooleanField(default=True)),
                ('country_code', models.CharField(max_length=10, null=True)),
                ('account_name', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
            ],
        ),
    ]

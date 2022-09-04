# Generated by Django 4.1 on 2022-09-04 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppPasswordRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("poll_token", models.CharField(max_length=128)),
                ("login_token", models.CharField(max_length=128)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="AuthenticatedAppPasswordRequest",
            fields=[
                (
                    "apppasswordrequest_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="app.apppasswordrequest",
                    ),
                ),
                ("artemis_user", models.CharField(max_length=50)),
            ],
            bases=("app.apppasswordrequest",),
        ),
    ]

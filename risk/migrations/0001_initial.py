
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=20, unique=True)),
                ('age', models.IntegerField()),
                ('diagnosis_code', models.CharField(max_length=20)),
                ('days_in_hospital', models.IntegerField()),
                ('num_medications', models.IntegerField()),
                ('previous_visits', models.IntegerField()),
                ('risk_score', models.FloatField(default=0)),
                ('risk_tier', models.CharField(default='LOW', max_length=6)),
                ('risk_factors', models.JSONField(default=list)),
                ('tasks', models.JSONField(default=list)),
                ('task_done', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-risk_score'],
            },
        ),
    ]

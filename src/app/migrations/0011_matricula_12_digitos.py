import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_teste_progresso_inscricao_resultado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='numero_matricula',
            field=models.CharField(
                max_length=12,
                unique=True,
                validators=[django.core.validators.RegexValidator('^\\d{12}$', 'A matrícula deve ter exatamente 12 dígitos numéricos.')],
            ),
        ),
    ]

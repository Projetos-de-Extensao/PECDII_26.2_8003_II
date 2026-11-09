import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def texto_para_fk(apps, schema_editor):
    Turma = apps.get_model('app', 'Turma')
    Materia = apps.get_model('app', 'Materia')
    for turma in Turma.objects.all():
        nome = (turma.materia_texto or '').strip()
        if not nome:
            continue
        materia, _ = Materia.objects.get_or_create(curso_id=turma.curso_id, nome=nome)
        turma.materia = materia
        turma.save(update_fields=['materia'])


def fk_para_texto(apps, schema_editor):
    Turma = apps.get_model('app', 'Turma')
    for turma in Turma.objects.select_related('materia'):
        turma.materia_texto = turma.materia.nome if turma.materia else ''
        turma.save(update_fields=['materia_texto'])


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_matricula_12_digitos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='app.curso')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('curso', 'nome'), name='materia_unica_por_curso')],
            },
        ),
        migrations.RenameField(
            model_name='turma',
            old_name='materia',
            new_name='materia_texto',
        ),
        migrations.AddField(
            model_name='turma',
            name='materia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='turmas', to='app.materia'),
        ),
        migrations.RunPython(texto_para_fk, fk_para_texto),
        migrations.RemoveField(
            model_name='turma',
            name='materia_texto',
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator('^\\d{12}$', 'A matrícula deve ter exatamente 12 dígitos numéricos.')])),
                ('aluno', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='matricula', to='app.aluno')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='matriculas', to='app.curso')),
                ('materias', models.ManyToManyField(blank=True, related_name='matriculas', to='app.materia')),
            ],
        ),
    ]

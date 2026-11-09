import django.db.models.deletion
from django.db import migrations, models


def texto_para_fk(apps, schema_editor):
    Sala = apps.get_model('app', 'Sala')
    Unidade = apps.get_model('app', 'Unidade')
    for sala in Sala.objects.all():
        nome = (sala.unidade_texto or '').strip() or 'Sem unidade'
        unidade, _ = Unidade.objects.get_or_create(nome=nome)
        sala.unidade = unidade
        sala.save(update_fields=['unidade'])


def fk_para_texto(apps, schema_editor):
    Sala = apps.get_model('app', 'Sala')
    for sala in Sala.objects.select_related('unidade'):
        sala.unidade_texto = sala.unidade.nome if sala.unidade else ''
        sala.save(update_fields=['unidade_texto'])


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_turma_materia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('endereco', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='sala',
            old_name='unidade',
            new_name='unidade_texto',
        ),
        migrations.AddField(
            model_name='sala',
            name='unidade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='salas', to='app.unidade'),
        ),
        migrations.AddField(
            model_name='curso',
            name='unidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cursos', to='app.unidade'),
        ),
        migrations.RunPython(texto_para_fk, fk_para_texto),
        migrations.RemoveField(
            model_name='sala',
            name='unidade_texto',
        ),
        migrations.AlterField(
            model_name='sala',
            name='unidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='salas', to='app.unidade'),
        ),
    ]

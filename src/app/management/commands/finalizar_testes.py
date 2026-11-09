from django.core.management.base import BaseCommand

from app.models import TesteProgresso


class Command(BaseCommand):
    help = "Finaliza os testes de progresso cuja data já passou."

    def handle(self, *args, **options):
        total = TesteProgresso.finalizar_vencidos()
        self.stdout.write(f"{total} teste(s) finalizado(s).")

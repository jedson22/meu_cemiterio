import os
import django

# Configura o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def setup():
    print("--- Iniciando Configuração do Banco ---")
    
    # 1. Cria as tabelas (Migrate)
    print("Rodando Migrations...")
    call_command('migrate', interactive=False)
    
    # 2. Cria o Superusuário se ele não existir
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("Criando superusuário 'admin'...")
        # ATENÇÃO: A senha será 'admin123'. Mude depois!
        User.objects.create_superuser('admin', 'admin@email.com', 'admin123')
    else:
        print("Superusuário 'admin' já existe.")

if __name__ == "__main__":
    setup()

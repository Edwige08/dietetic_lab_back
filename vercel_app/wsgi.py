import os
import sys
from pathlib import Path

# Ajoute le répertoire racine au Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ton_projet.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
app = application
import os
from celery import Celery

# Вказуємо шлях до налаштувань Django для програми Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Створюємо екземпляр Celery з назвою проекту
app = Celery('core')

# Завантажуємо налаштування з settings.py, що починаються з префіксу CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично шукаємо файли tasks.py у всіх твоїх додатках (backend.api, backend.accounts тощо)
app.autodiscover_tasks()
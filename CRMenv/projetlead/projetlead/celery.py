from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'create-appointment-reminders': {
        'task': 'notification.tasks.create_appointment_reminders',
        'schedule': crontab(hour=7, minute=0),  # Exécuter tous les jours à 7h00
    },
}
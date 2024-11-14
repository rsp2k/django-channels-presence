import logging

try:
    from celery import shared_task

    from channels_presence.models import Room

    @shared_task(name='channels_presence.tasks.prune_presence')
    def prune_presence():
        Room.objects.prune_presences()

    @shared_task(name='channels_presence.tasks.prune_rooms')
    def prune_rooms():
        Room.objects.prune_rooms()

except ImportError:
    logging.info(
        """Django Channels Presence 4.0\n
        You tried to use Celery tasks but it is not installed.
        """
    )


try:
    from huey import crontab
    from huey.contrib.djhuey import db_periodic_task, db_task

    @db_periodic_task(crontab(minute='*/1'))
    def prune_presence():
        Room.objects.prune_presences()

    @db_periodic_task(crontab(minute='*/10'))
    def prune_rooms():
        Room.objects.prune_rooms()

except ImportError:
    logging.info(
        """Django Channels Presence 4.0\n
        You tried to use huey tasks but it is not installed.
        """
    )

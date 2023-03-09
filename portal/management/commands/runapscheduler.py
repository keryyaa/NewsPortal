

# Так работало бы если не было бы celery


# import datetime
# import logging
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.core.management.base import BaseCommand
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from portal.models import Post, Category
# from django.template.loader import render_to_string
#
# logger = logging.getLogger(__name__)
#
# # Создаем функцию которая будет рассылать письма основываясь на том что делали в сигналах
# def my_job():
#     # Получаем время на момент запуска функции
#     today = datetime.datetime.now()
#     # Вычитаем из нового времени 7 дней
#     last_week = today - datetime.timedelta(days=7)
#     # Получаем обьекты модели Post с помощью фильтра применяем gte больше или равно
#     posts = Post.objects.filter(date_in__gte=last_week)
#     # Из постов достаем категории при чем flat помодет достать не словарь а кортеж значений как я понял
#     categories = set(posts.values_list('category__name', flat=True))
#     # Получаем email пользователей для того что бы отправить письма
#     subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribe__email', flat=True))
#     # А дальше все по схеме как в сигналах
#     html_content = render_to_string(
#         'email/CreateMassEmail.html',
#         {
#             'link': settings.SITE_URL,
#             'posts': posts,
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject='Новости за неделю',
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#     msg.attach_alternative(html_content, 'text/html',)
#     msg.send()
#
#
#
# # Скопировал с сайта skillfactory не совсем разобрался что как работает но разберусь обязательно
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     """
#     This job deletes APScheduler job execution entries older than `max_age`
#     from the database.
#     It helps to prevent the database from filling up with old historical
#     records that are no longer useful.
#
#     :param max_age: The maximum length of time to retain historical
#                     job execution records. Defaults to 7 days.
#     """
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # Ставим дату/время отправки
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")

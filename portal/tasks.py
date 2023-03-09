from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import datetime
from .models import Post, Category


@shared_task
def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string(
        'email/CreatePostEmail.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(
        html_context,
        'text/html',
    )
    msg.send()


@shared_task
def action_every_monday_8am():
    # Получаем время на момент запуска функции
    today = datetime.datetime.now()
    # Вычитаем из нового времени 7 дней
    last_week = today - datetime.timedelta(days=7)
    # Получаем обьекты модели Post с помощью фильтра применяем gte больше или равно
    posts = Post.objects.filter(date_in__gte=last_week)
    # Из постов достаем категории при чем flat помодет достать не словарь а кортеж значений как я понял
    categories = set(posts.values_list('category__name', flat=True))
    # Получаем email пользователей для того что бы отправить письма
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribe__email', flat=True))
    # А дальше все по схеме как в сигналах
    html_content = render_to_string(
        'email/CreateMassEmail.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html', )
    msg.send()

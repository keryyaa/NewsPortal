from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from portal.models import PostCategory
from news.settings import SITE_URL, DEFAULT_FROM_EMAIL


def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string(
        'email/CreatePostEmail.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(
        html_context,
        'text/html',
    )
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_save(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribe.all()

        subscribers = [user.email for user in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers)


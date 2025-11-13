from django.db import models
from solo.models import SingletonModel


class BusinessConfig(SingletonModel):
	saplings_in_hectare = models.PositiveSmallIntegerField(default = 1000,
		help_text='Используется в калькуляторе стоимости')
	new_feedback_requests_receiver_emails = models.TextField(
		default='vlad.buklovsky@gmail.com',
		help_text='Почты тех, кому будет отправлено уведомление о новой заявке, раздёлённые знаком запятой ",".'
	)

	class Meta:
		verbose_name = '🛠 | Конфиг бизнес параметров'
	def __str__(self): return self._meta.verbose_name

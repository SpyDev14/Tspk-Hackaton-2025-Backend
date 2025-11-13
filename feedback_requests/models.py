# Я решил не создавать отдельную папку т.к тут будет максимум 1-2 модели, не более.
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class FeedbackRequest(models.Model):
	requestener_name = models.CharField("Имя", max_length = 24)
	phone_number = PhoneNumberField("Номер телефона")
	email = models.EmailField('Почта', blank = True)
	comment = models.TextField('Комментарий', blank=True, max_length = 512)
	seen = models.BooleanField("Увидено персоналом", default=False, help_text=(
		'Если уведомление о создании новой заявки успешно ушло '
		'в телеграм — автоматически считается "Увиденным". '
		'Иначе, считается что заявку не увидели и нужно вручную '
		'поставить эту галочку админке, когда её увидят.'
	))
	created_at = models.DateTimeField("Дата заполнения заявки", auto_now_add = True)

	class Meta:
		verbose_name = 'Заявка на обратную связь'
		verbose_name_plural = 'Заявки на обратную связь'

	def __str__(self):
		return f'Заявка от {self.requestener_name} {self.phone_number}'

	def mark_as_seen(self):
		"""Устанавливает True в seen и сохраняет, если ещё не было seen."""
		if self.seen:
			return
		self.seen = True
		self.save(update_fields=('seen',))

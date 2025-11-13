from django.core.validators import MinValueValidator
from django.db 				import models

from core.models.bases import OrderedModel, UniqueNamedModel


class HectarePatronageBonus(UniqueNamedModel, OrderedModel):
	class Meta(OrderedModel.Meta):
		verbose_name = 'бонус'
		verbose_name_plural = 'бонусы шефства над гектарами'

class HectarePatronageManager(models.Manager):
	def prefetched(self):
		self.prefetch_related('bonuses')

class HectarePatronage(models.Model):
	# Без дробной
	hectares = models.PositiveSmallIntegerField('Количество гектар', unique=True,
		default=1, validators=[MinValueValidator(1)])
	price_in_thousands = models.PositiveSmallIntegerField('Цена в тысячах',
		default=25, validators=[MinValueValidator(1)])
	bonuses = models.ManyToManyField(HectarePatronageBonus, verbose_name='Бонусы')
	summary = models.TextField('Краткое описание', max_length=256)

	class Meta:
		ordering = ['hectares']
		verbose_name = 'шефство гектара'
		verbose_name_plural = 'варианты шефства гектаров'

	def __str__(self):
		return f"{self.hectares} {self._get_declensed_hectare().capitalize()}"

	@property
	def price(self):
		return self.price_in_thousands * 1000

	def _get_declensed_hectare(self) -> str:
		last_digit = self.hectares % 10
		last_two_digits = self.hectares % 100

		if 11 <= last_two_digits <= 19:
			return 'гектаров'
		elif last_digit == 1:
			return 'гектар'
		elif 2 <= last_digit <= 4:
			return 'гектара'
		else: return 'гектаров'

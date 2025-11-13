from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline

from shared.admin.model_registration 	import AdminModelRegistrator
from core.admin.mixins 					import DynamicExtraMixin
from core.admin.bases 					import OrderedModelAdmin
from business.apps 						import BusinessConfig
from business 							import models


registrator = AdminModelRegistrator(
	app_name = BusinessConfig.name
)

# FIXME: Исправить exclude_inline_model
# @registrator.exclude_inline_model
# registrator.exclude_model(models.HectarePatronageBonus)
# class HectarePatronageBonusInline(DynamicExtraMixin, SortableTabularInline):
# 	model = models.HectarePatronageBonus

# @registrator.set_for_model(models.HectarePatronage)
# class HectarePatronageAdmin(OrderedModelAdmin):
# 	inlines = [HectarePatronageBonusInline]

@registrator.set_for_model(models.HectarePatronageBonus)
class HectarePatronageBonusAdmin(OrderedModelAdmin):
	list_display = ['name', 'edit']
	list_editable = ['name']
	list_display_links = ['edit']

	def edit(*args):
		return '[Редактировать]'
	edit.short_description = models.HectarePatronageBonus._meta.verbose_name

registrator.register()

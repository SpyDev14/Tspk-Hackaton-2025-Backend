from core.views.bases import PageWithFormView, ConcretePageView

from business.views.mixins 	import FeedbackRequestFormMixin
from business 				import models


class HomePageView(FeedbackRequestFormMixin, PageWithFormView):
	template_name = 'business/index.html'
	page_slug = 'index'

	def get_context_data(self, **kwargs):
		return super().get_context_data(
			last_articles = models.Article.objects.published()[:5],
			hectare_patronage = models.HectarePatronage.objects.prefetched(),
			services = models.Service.objects.all(),
			**kwargs
		)

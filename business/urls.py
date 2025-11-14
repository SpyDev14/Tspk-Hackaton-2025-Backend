from rest_framework.routers import DefaultRouter
from django.urls 			import path, include

from business import views
from business.api.views import SaplingsCalculatorViewSet

api_router = DefaultRouter()
api_router.register('patronage/<int:hectares>/', SaplingsCalculatorViewSet, basename='patronage')

# Формат name: modelname-type
urlpatterns = [
	path('', views.HomePageView.as_view(), name = 'index'),

	# Models
	path('blog/', views.ArticleListView.as_view(), name = 'article-list'),
	path('blog/<slug:slug>/', views.ArticleDetailView.as_view(), name = 'article-detail'),

	# Api endpoints
	path('api/', include(api_router.urls))
]

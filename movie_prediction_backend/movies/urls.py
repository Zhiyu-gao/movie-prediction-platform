from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, MoviePredictionView

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', MoviePredictionView.as_view({'post': 'create'}), name='movie-predict'),
]
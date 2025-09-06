from rest_framework import serializers
from .models import MovieGenreClassificationFinal

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenreClassificationFinal
        fields = '__all__'

class MoviePredictionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    year = serializers.IntegerField(min_value=1900, max_value=2030)
    director = serializers.CharField(max_length=255)
    duration = serializers.IntegerField(min_value=60, max_value=300)
    genre = serializers.CharField(max_length=100)
    content_rating = serializers.CharField(max_length=20)
    lead_actor = serializers.CharField(max_length=255)
    budget = serializers.DecimalField(max_digits=15, decimal_places=2)
    rating = serializers.FloatField(min_value=0.0, max_value=10.0)
    votes = serializers.IntegerField(min_value=1000)
    language = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    production_company = serializers.CharField(max_length=255)
    num_awards = serializers.IntegerField(min_value=0)
    critic_reviews = serializers.IntegerField(min_value=0)
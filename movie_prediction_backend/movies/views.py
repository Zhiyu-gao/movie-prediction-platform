# type: ignore
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Avg, Sum
from .models import MovieGenreClassificationFinal
from .serializers import MovieSerializer, MoviePredictionSerializer
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import os
from typing import Any, Dict, List, Optional

class MovieViewSet(viewsets.ModelViewSet):
    queryset = MovieGenreClassificationFinal.objects.all()  # type: ignore
    serializer_class = MovieSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索电影"""
        query = request.query_params.get('q', '')
        if query:
            movies = self.queryset.filter(
                Q(title__icontains=query) |  
                Q(director__icontains=query) | 
                Q(genre__icontains=query)  
            )
        else:
            movies = self.queryset.all()
        
        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取电影统计数据"""
        total_movies = self.queryset.count()
        avg_rating = self.queryset.aggregate(avg_rating=Avg('rating'))['avg_rating']
        total_budget = self.queryset.aggregate(total_budget=Sum('budget_usd'))['total_budget']
        total_boxoffice = self.queryset.aggregate(total_boxoffice=Sum('boxoffice_usd'))['total_boxoffice']
        
        return Response({
            'total_movies': total_movies,
            'average_rating': round(avg_rating, 2) if avg_rating else 0,
            'total_budget': total_budget or 0,
            'total_boxoffice': total_boxoffice or 0
        })

class MoviePredictionView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model: Optional[RandomForestRegressor] = None
        self.scaler: Optional[StandardScaler] = None
        self.load_model()
    
    def load_model(self) -> None:
        """加载或训练预测模型"""
        model_path = 'movie_prediction_model.pkl'
        scaler_path = 'movie_scaler.pkl'
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                print("模型加载成功")
            except Exception as e:
                print(f"模型加载失败: {e}")
                self.train_model()
        else:
            self.train_model()
    
    def train_model(self) -> None:
        """训练票房预测模型"""
        try:
            movies = MovieGenreClassificationFinal.objects.all()  # type: ignore
            data: List[Dict[str, Any]] = []
            for movie in movies:
                try:
                    year = int(movie.year) if movie.year and movie.year.isdigit() else 2020
                    duration = int(movie.duration) if movie.duration and movie.duration.isdigit() else 120
                    rating = float(movie.rating) if movie.rating and movie.rating.replace('.', '').isdigit() else 7.0
                    votes = int(movie.votes) if movie.votes and movie.votes.isdigit() else 10000
                    num_awards = int(movie.num_awards) if movie.num_awards and movie.num_awards.isdigit() else 0
                    critic_reviews = int(movie.critic_reviews) if movie.critic_reviews and movie.critic_reviews.isdigit() else 100
                    budget_usd = float(movie.budget_usd) if movie.budget_usd and movie.budget_usd.replace('.', '').isdigit() else 50000000
                    boxoffice_usd = float(movie.boxoffice_usd) if movie.boxoffice_usd and movie.boxoffice_usd.replace('.', '').isdigit() else budget_usd
                    genre = str(movie.genre).strip() if movie.genre else 'Action'
                    data.append({
                        'year': year,
                        'duration': duration,
                        'rating': rating,
                        'votes': votes,
                        'num_awards': num_awards,
                        'critic_reviews': critic_reviews,
                        'budget_usd': budget_usd,
                        'genre': genre,
                        'boxoffice_usd': boxoffice_usd
                    })
                except (ValueError, AttributeError):
                    continue
            if len(data) < 10:
                data = self.get_default_training_data()
            df = pd.DataFrame(data)
            X = df[['year', 'duration', 'rating', 'votes', 'num_awards', 'critic_reviews']]
            y = df['boxoffice_usd']
            print("--------------------")
            print("y的值为")
            print(y)
            print("---------------")

            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_scaled, y)
            joblib.dump(self.model, 'movie_prediction_model.pkl')
            joblib.dump(self.scaler, 'movie_scaler.pkl')
            print("模型训练完成")
        except Exception as e:
            print(f"模型训练失败: {e}")
            self.model = None
            self.scaler = None
    
    def get_default_training_data(self) -> List[Dict[str, Any]]:
        """获取默认训练数据"""
        return [
            {'year': 2020, 'duration': 120, 'rating': 7.5, 'votes': 50000, 'num_awards': 2, 'critic_reviews': 150, 'budget_usd': 50000000},
            {'year': 2021, 'duration': 130, 'rating': 8.0, 'votes': 75000, 'num_awards': 5, 'critic_reviews': 200, 'budget_usd': 75000000},
            {'year': 2022, 'duration': 110, 'rating': 6.8, 'votes': 30000, 'num_awards': 1, 'critic_reviews': 100, 'budget_usd': 30000000},
            {'year': 2023, 'duration': 140, 'rating': 8.5, 'votes': 100000, 'num_awards': 8, 'critic_reviews': 300, 'budget_usd': 100000000},
            {'year': 2024, 'duration': 125, 'rating': 7.2, 'votes': 60000, 'num_awards': 3, 'critic_reviews': 180, 'budget_usd': 60000000},
        ]
    
    def create(self, request):
        """进行票房预测"""
        serializer = MoviePredictionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                features = np.array([[
                    data['year'],
                    data['duration'],
                    data['rating'],
                    data['votes'],
                    data['num_awards'],
                    data['critic_reviews']
                ]])
                if self.scaler is not None:
                    features_scaled = self.scaler.transform(features)
                else:
                    return Response({'error': '模型未正确初始化'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                if self.model is not None:
                    predicted_boxoffice = self.model.predict(features_scaled)[0]
                else:
                    return Response({'error': '模型未正确初始化'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                confidence = 80.0
                roi = ((predicted_boxoffice - float(data['budget'])) / float(data['budget'])) * 100 if float(data['budget']) > 0 else 0
                return Response({
                    'predicted_boxoffice': round(predicted_boxoffice, 2),
                    'confidence': round(confidence, 2),
                    'roi': round(roi, 2)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'预测失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
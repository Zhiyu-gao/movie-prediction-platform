# type: ignore
# 训练模型脚本 - 使用真实数据库数据
import os
import sys
import django
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_prediction_backend.settings')
django.setup()

from movies.models import MovieGenreClassificationFinal

def load_data_from_database():
    """从数据库加载真实数据"""
    print("正在从数据库加载数据...")
    
    movies = MovieGenreClassificationFinal.objects.all()
    data = []
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
        except (ValueError, AttributeError) as e:
            continue
    print(f"成功加载 {len(data)} 条有效数据")
    return pd.DataFrame(data)

def create_enhanced_features(df):
    """创建增强特征"""
    # 基础特征
    features = df[['year', 'duration', 'rating', 'votes', 'num_awards', 'critic_reviews']].copy()
    
    # 添加衍生特征
    features['rating_votes_ratio'] = df['rating'] * np.log(df['votes'])
    features['awards_per_review'] = df['num_awards'] / (df['critic_reviews'] + 1)
    features['year_factor'] = (df['year'] - 1900) / 130  # 年份标准化
    features['duration_factor'] = df['duration'] / 180  # 时长标准化
    
    # 处理无穷大和NaN值
    features = features.replace([np.inf, -np.inf], np.nan)
    features = features.fillna(features.mean())
    
    return features

def train_model():
    """训练票房预测回归模型"""
    print("开始训练模型...")
    df = load_data_from_database()
    if len(df) < 10:
        print("数据不足，使用默认训练数据...")
        df = get_default_training_data()
    X = create_enhanced_features(df)
    y = df['boxoffice_usd']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print("y_train的值为...........")
    print(y_train)
    print("--------------------------")
    print("y_test的值为...........")
    print(y_test)
    print("......................")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mse = ((y_pred - y_test) ** 2).mean()
    print(f"模型均方误差: {mse:.2f}")
    joblib.dump(model, 'movie_prediction_model.pkl')
    joblib.dump(scaler, 'movie_scaler.pkl')
    print("\n模型训练完成！")
    print("保存的文件:")
    print("- movie_prediction_model.pkl")
    print("- movie_scaler.pkl")
    return model, scaler

def get_default_training_data():
    """获取默认训练数据（基于真实电影数据）"""
    return pd.DataFrame([
        {'year': 2009, 'duration': 162, 'rating': 7.8, 'votes': 1200000, 'num_awards': 3, 'critic_reviews': 350, 'budget_usd': 237000000},  # 阿凡达
        {'year': 1997, 'duration': 194, 'rating': 7.9, 'votes': 1100000, 'num_awards': 11, 'critic_reviews': 280, 'budget_usd': 200000000},  # 泰坦尼克号
        {'year': 2019, 'duration': 181, 'rating': 8.4, 'votes': 1000000, 'num_awards': 1, 'critic_reviews': 450, 'budget_usd': 356000000},  # 复仇者联盟4
        {'year': 2015, 'duration': 138, 'rating': 7.9, 'votes': 900000, 'num_awards': 0, 'critic_reviews': 400, 'budget_usd': 245000000},  # 星球大战7
        {'year': 2018, 'duration': 149, 'rating': 8.4, 'votes': 950000, 'num_awards': 0, 'critic_reviews': 420, 'budget_usd': 321000000},  # 复仇者联盟3
        {'year': 2012, 'duration': 164, 'rating': 8.0, 'votes': 1500000, 'num_awards': 4, 'critic_reviews': 500, 'budget_usd': 250000000},  # 黑暗骑士崛起
        {'year': 2010, 'duration': 148, 'rating': 8.8, 'votes': 2500000, 'num_awards': 2, 'critic_reviews': 600, 'budget_usd': 160000000},  # 盗梦空间
        {'year': 2008, 'duration': 152, 'rating': 9.0, 'votes': 2500000, 'num_awards': 2, 'critic_reviews': 550, 'budget_usd': 185000000},  # 黑暗骑士
        {'year': 2003, 'duration': 201, 'rating': 8.9, 'votes': 1800000, 'num_awards': 11, 'critic_reviews': 400, 'budget_usd': 94000000},  # 指环王3
        {'year': 2001, 'duration': 178, 'rating': 8.8, 'votes': 1800000, 'num_awards': 4, 'critic_reviews': 350, 'budget_usd': 93000000},  # 指环王1
    ])

if __name__ == '__main__':
    try:
        model, scaler = train_model()
        print("\n模型训练成功完成！")
    except Exception as e:
        print(f"模型训练失败: {e}")
        sys.exit(1)
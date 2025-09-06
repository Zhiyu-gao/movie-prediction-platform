# 数据导入脚本 - 将CSV数据导入到Django数据库
import os
import sys
import django
import pandas as pd
from django.db import transaction
from typing import List, Dict, Any, Union

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_prediction_backend.settings')
django.setup()

from movies.models import MovieGenreClassificationFinal

def clean_data(value: Any) -> Union[str, None]:
    """清理数据值"""
    if pd.isna(value) or value == '' or value == 'nan':
        return None
    return str(value).strip()

def create_sample_data() -> None:
    """创建示例数据"""
    print("创建示例数据...")
    
    sample_movies: List[Dict[str, str]] = [
        {
            'title': '阿凡达',
            'year': '2009',
            'director': '詹姆斯·卡梅隆',
            'duration': '162',
            'rating': '7.8',
            'votes': '1200000',
            'description': '潘多拉星球上的科幻冒险',
            'language': '英语',
            'country': '美国',
            'budget_usd': '237000000',
            'boxoffice_usd': '2847246203',
            'genre': '科幻',
            'production_company': '20世纪福克斯',
            'content_rating': 'PG-13',
            'lead_actor': '萨姆·沃辛顿',
            'num_awards': '3',
            'critic_reviews': '350'
        },
        {
            'title': '泰坦尼克号',
            'year': '1997',
            'director': '詹姆斯·卡梅隆',
            'duration': '194',
            'rating': '7.9',
            'votes': '1100000',
            'description': '1912年泰坦尼克号沉船的爱情故事',
            'language': '英语',
            'country': '美国',
            'budget_usd': '200000000',
            'boxoffice_usd': '2201647264',
            'genre': '爱情',
            'production_company': '派拉蒙影业',
            'content_rating': 'PG-13',
            'lead_actor': '莱昂纳多·迪卡普里奥',
            'num_awards': '11',
            'critic_reviews': '280'
        },
        {
            'title': '复仇者联盟4：终局之战',
            'year': '2019',
            'director': '安东尼·罗素',
            'duration': '181',
            'rating': '8.4',
            'votes': '1000000',
            'description': '漫威超级英雄的终极集结',
            'language': '英语',
            'country': '美国',
            'budget_usd': '356000000',
            'boxoffice_usd': '2797501328',
            'genre': '动作',
            'production_company': '漫威影业',
            'content_rating': 'PG-13',
            'lead_actor': '小罗伯特·唐尼',
            'num_awards': '1',
            'critic_reviews': '450'
        },
        {
            'title': '星球大战：原力觉醒',
            'year': '2015',
            'director': 'J·J·艾布拉姆斯',
            'duration': '138',
            'rating': '7.9',
            'votes': '900000',
            'description': '星球大战系列第七部',
            'language': '英语',
            'country': '美国',
            'budget_usd': '245000000',
            'boxoffice_usd': '2068223624',
            'genre': '科幻',
            'production_company': '卢卡斯影业',
            'content_rating': 'PG-13',
            'lead_actor': '黛西·雷德利',
            'num_awards': '0',
            'critic_reviews': '400'
        },
        {
            'title': '复仇者联盟3：无限战争',
            'year': '2018',
            'director': '安东尼·罗素',
            'duration': '149',
            'rating': '8.4',
            'votes': '950000',
            'description': '复仇者联盟与灭霸的终极对决',
            'language': '英语',
            'country': '美国',
            'budget_usd': '321000000',
            'boxoffice_usd': '2048359754',
            'genre': '动作',
            'production_company': '漫威影业',
            'content_rating': 'PG-13',
            'lead_actor': '小罗伯特·唐尼',
            'num_awards': '0',
            'critic_reviews': '420'
        }
    ]
    
    movies_to_create = []
    for movie_data in sample_movies:
        movies_to_create.append(MovieGenreClassificationFinal(**movie_data))
    
    with transaction.atomic():  # type: ignore
        MovieGenreClassificationFinal.objects.bulk_create(  # type: ignore
            movies_to_create,
            ignore_conflicts=True
        )
    
    print(f"成功创建 {len(sample_movies)} 条示例数据")

if __name__ == '__main__':
    print("开始导入数据...")
    create_sample_data()
    print("数据导入完成！") 
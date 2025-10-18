"""
Module thu thập và xử lý dữ liệu thời tiết từ API
"""

import requests
import pandas as pd
from datetime import datetime
import streamlit as st

# CONSTANTS
CITIES = {
    'Hà Nội': {'lat': 21.0285, 'lon': 105.8542, 'region': 'Bắc'},
    'Hồ Chí Minh': {'lat': 10.8231, 'lon': 106.6297, 'region': 'Nam'},
    'Đà Nẵng': {'lat': 16.0544, 'lon': 108.2022, 'region': 'Trung'},
    'Hải Phòng': {'lat': 20.8449, 'lon': 106.6881, 'region': 'Bắc'},
    'Cần Thơ': {'lat': 10.0452, 'lon': 105.7469, 'region': 'Nam'},
    'Huế': {'lat': 16.4637, 'lon': 107.5909, 'region': 'Trung'},
    'Nha Trang': {'lat': 12.2388, 'lon': 109.1967, 'region': 'Trung'},
    'Vũng Tàu': {'lat': 10.3460, 'lon': 107.0843, 'region': 'Nam'}
}


# HELPER FUNCTIONS
def get_season(month):
    """Xác định mùa từ tháng"""
    if month in [12, 1, 2]:
        return 'Đông'
    elif month in [3, 4, 5]:
        return 'Xuân'
    elif month in [6, 7, 8]:
        return 'Hè'
    else:
        return 'Thu'


# DATA FETCHING
@st.cache_data(ttl=3600)
def fetch_weather_data(start_date='2025-01-01', end_date=None):
    """
    Thu thập dữ liệu thời tiết từ Open-Meteo API
    
    Args:
        start_date: Ngày bắt đầu (YYYY-MM-DD), mặc định 2025-01-01
        end_date: Ngày kết thúc (YYYY-MM-DD), mặc định là hôm nay
    
    Returns:
        DataFrame chứa dữ liệu thời tiết
    """
    # Nếu không chỉ định end_date, dùng ngày hôm nay
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    all_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_cities = len(CITIES)
    
    for idx, (city, coords) in enumerate(CITIES.items()):
        try:
            status_text.text(f'🌍 Đang tải dữ liệu {city}... ({idx+1}/{total_cities})')
            progress_bar.progress((idx + 1) / total_cities)
            
            # Open-Meteo API (Free, không cần API key)
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'start_date': start_date,
                'end_date': end_date,
                'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean,windspeed_10m_max',
                'timezone': 'Asia/Bangkok'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                dates = pd.to_datetime(data['daily']['time'])
                
                for i, date in enumerate(dates):
                    all_data.append({
                        'city': city,
                        'date': date,
                        'temp_max': data['daily']['temperature_2m_max'][i],
                        'temp_min': data['daily']['temperature_2m_min'][i],
                        'temp_mean': data['daily']['temperature_2m_mean'][i],
                        'rainfall': data['daily']['precipitation_sum'][i],
                        'humidity': data['daily']['relative_humidity_2m_mean'][i],
                        'windspeed': data['daily']['windspeed_10m_max'][i],
                        'lat': coords['lat'],
                        'lon': coords['lon'],
                        'region': coords['region']
                    })
            else:
                st.warning(f"⚠️ Không thể lấy dữ liệu cho {city} (Status: {response.status_code})")
                
        except Exception as e:
            st.error(f"❌ Lỗi khi lấy dữ liệu {city}: {str(e)}")
    
    progress_bar.empty()
    status_text.empty()
    
    if not all_data:
        st.error("❌ Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet.")
        return pd.DataFrame()
    
    df = pd.DataFrame(all_data)
    
    # Feature Engineering
    df = add_features(df)
    
    # st.success(f"✅ Đã tải {len(df):,} điểm dữ liệu từ {total_cities} thành phố!")
    
    return df


# FEATURE ENGINEERING
def add_features(df):
    """
    Thêm các cột đặc trưng mới
    
    Args:
        df: DataFrame gốc
    
    Returns:
        DataFrame với các cột mới
    """
    if df.empty:
        return df
    
    # Thời gian
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['dayofweek'] = df['date'].dt.dayofweek
    df['season'] = df['month'].apply(get_season)
    
    # Nhiệt độ
    df['temp_range'] = df['temp_max'] - df['temp_min']
    df['temp_category'] = pd.cut(
        df['temp_mean'], 
        bins=[0, 20, 28, 100], 
        labels=['Mát', 'Ấm', 'Nóng']
    )
    
    # Độ ẩm
    df['humidity_level'] = pd.cut(
        df['humidity'], 
        bins=[0, 60, 80, 100], 
        labels=['Thấp', 'TB', 'Cao']
    )
    
    # Mưa
    df['rain_category'] = pd.cut(
        df['rainfall'], 
        bins=[0, 5, 20, 1000], 
        labels=['Ít', 'Vừa', 'Nhiều']
    )
    
    # Gió
    df['wind_category'] = pd.cut(
        df['windspeed'],
        bins=[0, 20, 40, 100],
        labels=['Nhẹ', 'Vừa', 'Mạnh']
    )
    
    # Comfort index (đơn giản hóa)
    df['comfort_index'] = 100 - abs(df['temp_mean'] - 25) * 3 - abs(df['humidity'] - 60) / 2
    
    return df


# DATA FILTERING

def filter_data(df, cities=None, date_range=None, season=None):
    """
    Lọc dữ liệu theo các tiêu chí
    
    Args:
        df: DataFrame gốc
        cities: List thành phố cần lọc
        date_range: Tuple (start_date, end_date)
        season: Mùa cần lọc
    
    Returns:
        DataFrame đã lọc
    """
    df_filtered = df.copy()
    
    if cities:
        df_filtered = df_filtered[df_filtered['city'].isin(cities)]
    
    if date_range:
        start, end = date_range
        df_filtered = df_filtered[
            (df_filtered['date'] >= pd.Timestamp(start)) & 
            (df_filtered['date'] <= pd.Timestamp(end))
        ]
    
    if season and season != 'Tất cả':
        df_filtered = df_filtered[df_filtered['season'] == season]
    
    return df_filtered


# STATISTICS
def get_statistics(df):
    """
    Tính toán các thống kê cơ bản
    
    Returns:
        Dictionary chứa các thống kê
    """
    if df.empty:
        return {}
    
    stats = {
        'avg_temp': df['temp_mean'].mean(),
        'max_temp': df['temp_max'].max(),
        'min_temp': df['temp_min'].min(),
        'avg_humidity': df['humidity'].mean(),
        'total_rainfall': df['rainfall'].sum(),
        'avg_rainfall': df['rainfall'].mean(),
        'avg_windspeed': df['windspeed'].mean(),
        'hottest_city': df.groupby('city')['temp_mean'].mean().idxmax(),
        'coldest_city': df.groupby('city')['temp_mean'].mean().idxmin(),
        'rainiest_city': df.groupby('city')['rainfall'].sum().idxmax(),
        'driest_city': df.groupby('city')['rainfall'].sum().idxmin(),
    }
    
    return stats
"""
Dashboard Phân Tích Thời Tiết các thành phố lớn Việt Nam 2025
Main Application File
"""

import streamlit as st
from datetime import datetime

# Import modules
from data_fetcher import fetch_weather_data, filter_data, CITIES
from tab_overview import render_tab_overview
from tab_trends import render_tab_trends
from tab_temperature import render_tab_temperature
from tab_rainfall import render_tab_rainfall
from tab_map import render_tab_map
from tab_comparison import render_tab_comparison

# PAGE CONFIG
st.set_page_config(
    page_title="Thời tiết Việt Nam 2025",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stMetric {
        background: #1078A8;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stMetric label {
        color: white !important;
    }
    .stMetric .metric-value {
        color: white !important;
    }
    h1 {
        color: #667eea;
    }
    h2 {
        color: #764ba2;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background: #074D9C;
        color: white;
    }
    .st-emotion-cache-1ffuo7c {
        height: 20px;
    }
    /* Giảm khoảng trắng đầu trang */
    .st-emotion-cache-zy6yx3 {
        padding-top: 16px !important;
    }

    /* Xoá margin dưới tiêu đề hoặc các container không mong muốn */
    .st-emotion-cache-10p9htt {
        margin-bottom: 0 !important;
        
    }
    .st-emotion-cache-1fwbbrh > h1 {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }
   
    
    .st-emotion-cache-zy6yx3 {
        padding-bottom: 0 !important;
    }
    

    

    
    
    
    

   
</style>
""", unsafe_allow_html=True)







# TITLE
st.title("🌤️Thời tiết các thành phố lớn Việt Nam 2025")
# st.markdown("### 📊 Dữ liệu thực từ Open-Meteo API")
st.markdown("---")

# LOAD DATA
@st.cache_data(ttl=3600, show_spinner=False)
def load_data_cached():
    return fetch_weather_data()

with st.spinner('🌍 Đang tải dữ liệu thời tiết từ API...'):
    df = load_data_cached()

if df.empty:
    st.error("⚠️ Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet và thử lại.")
    st.stop()

# SIDEBAR - FILTERS
st.sidebar.title("🎛️ Bộ Lọc Dữ Liệu")
st.sidebar.markdown("---")

# City filter
selected_cities = st.sidebar.multiselect(
    "📍 Chọn thành phố",
    options=list(CITIES.keys()),
    default=list(CITIES.keys()),
    help="Chọn một hoặc nhiều thành phố để phân tích"
)

# Date range filter
date_range = st.sidebar.date_input(
    "📅 Khoảng thời gian",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max(),
    help="Chọn khoảng thời gian cần phân tích"
)

# Season filter
selected_season = st.sidebar.selectbox(
    "🍂 Mùa",
    options=['Tất cả', 'Xuân', 'Hè', 'Thu', 'Đông'],
    help="Lọc dữ liệu theo mùa"
)

st.sidebar.markdown("---")

# FILTER DATA
df_filtered = filter_data(
    df,
    cities=selected_cities if selected_cities else None,
    date_range=date_range,
    season=selected_season
)

# Data info
st.sidebar.info(f"""
📊 **Thống kê dữ liệu:**
- Số điểm dữ liệu: **{len(df_filtered):,}**
- Số thành phố: **{df_filtered['city'].nunique()}**
- Từ ngày: **{df_filtered['date'].min().strftime('%d/%m/%Y')}**
- Đến ngày: **{df_filtered['date'].max().strftime('%d/%m/%Y')}**
""")

# Download button
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Tải Dữ Liệu")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

csv = convert_df_to_csv(df_filtered)

st.sidebar.download_button(
    label="⬇️ Tải CSV",
    data=csv,
    file_name=f'weather_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
    mime='text/csv',
    help="Tải dữ liệu đã lọc dưới dạng CSV"
)

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Tổng Quan",
    "📈 Xu Hướng Thời Gian",
    "🌡️ Phân Tích Nhiệt Độ",
    "💧 Phân Tích Độ Ẩm & Mưa",
    "🔍 So Sánh & Tương Quan",
    "🗺️ Bản Đồ Tương Tác",
])

# Render tabs
with tab1:
    render_tab_overview(df_filtered)

with tab2:
    render_tab_trends(df_filtered)

with tab3:
    render_tab_temperature(df_filtered)

with tab4:
    render_tab_rainfall(df_filtered)

with tab5:
    render_tab_comparison(df_filtered)

with tab6:
    render_tab_map(df_filtered)


# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌍 Dữ liệu từ <a href='https://open-meteo.com/' target='_blank'>Open-Meteo API</a> | 📅 Năm 2025</p>
    <p style='margin-top: 10px;'>Made with ❤️ by Quang Huy for Data Visualization</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR FOOTER
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📖 Hướng dẫn sử dụng

1. **Chọn bộ lọc** ở sidebar
2. **Khám phá 6 tabs** với các phân tích khác nhau
3. **Tương tác** với biểu đồ (zoom, hover, click)
4. **Tải dữ liệu** để phân tích offline

---

💡 **Tips:** Hover chuột lên biểu đồ để xem chi tiết!
""")

# ERROR HANDLING
if len(df_filtered) == 0:
    st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc. Vui lòng điều chỉnh các tiêu chí lọc.")
    
    
    
    
    
    
    
    
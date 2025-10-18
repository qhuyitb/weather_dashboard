"""
Tab 3: Phân Tích Nhiệt Độ
"""

import streamlit as st
import plotly.express as px
from visualizations import (
    create_scatter_with_regression,
    create_heatmap_calendar,
    create_boxplot
)

def render_tab_temperature(df_filtered):
    """Render tab phân tích nhiệt độ"""
    
    st.header("🌡️ Phân Tích Chi Tiết Nhiệt Độ")
    
    # SCATTER WITH REGRESSION
    st.subheader(" Scatter Plot - Nhiệt Độ vs Độ Ẩm (với Hồi Quy)")
    
    fig = create_scatter_with_regression(
        df_filtered,
        'temp_mean',
        'humidity',
        'city',
        'rainfall'
    )
    # Đổi title của biểu đồ sang tiếng Việt
    fig.update_layout(
        title='Mối quan hệ Nhiệt độ - Độ ẩm',
        xaxis_title='Nhiệt độ trung bình (°C)',
        yaxis_title='Độ ẩm (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate correlation
    corr = df_filtered[['temp_mean', 'humidity']].corr().iloc[0, 1]
    st.info(f" **Hệ số tương quan:** {corr:.3f} ({'Tương quan âm' if corr < 0 else 'Tương quan dương'})")
    
    # HEATMAP CALENDAR
    st.subheader(" Heatmap Lịch - Nhiệt Độ Theo Ngày")
    
    selected_cities = df_filtered['city'].unique().tolist()
    if selected_cities:
        city = st.selectbox("Chọn thành phố xem heatmap:", selected_cities, key='heatmap_city')
        fig = create_heatmap_calendar(df_filtered, city)
        st.plotly_chart(fig, use_container_width=True)
    
    # TEMPERATURE RANGE ANALYSIS
    st.subheader(" Phân Tích Biên Độ Nhiệt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_boxplot(
            df_filtered,
            'season',
            'temp_range',
            'Biên độ nhiệt theo mùa',
            'region'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        df_range = df_filtered.groupby('city')['temp_range'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=df_range.values,
            y=df_range.index,
            orientation='h',
            title='Biên độ nhiệt trung bình theo thành phố',
            labels={'x': 'Biên độ (°C)', 'y': 'Thành phố'},
            color=df_range.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
"""
Tab 4: Phân Tích Độ Ẩm & Mưa
"""

import streamlit as st
import plotly.express as px
from visualizations import (
    create_treemap,
    create_sunburst
)

def render_tab_rainfall(df_filtered):
    """Render tab phân tích độ ẩm & mưa"""
    
    st.header("💧 Phân Tích Độ Ẩm & Lượng Mưa")
    
    # ===========================
    # TREEMAP
    # ===========================
    st.subheader(" Treemap - Tổng Lượng Mưa Theo Thành Phố")
    
    fig = create_treemap(
        df_filtered,
        ['region', 'city'],
        'rainfall',
        'Phân bố lượng mưa (Treemap)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ===========================
    # SUNBURST
    # ===========================
    st.subheader(" Sunburst - Phân Bố Mưa Theo Mùa & Thành Phố")
    
    fig = create_sunburst(df_filtered)
    st.plotly_chart(fig, use_container_width=True)
    
    # ===========================
    # RAINFALL STATISTICS
    # ===========================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Top Thành Phố Mưa Nhiều")
        top_rain = df_filtered.groupby('city')['rainfall'].sum().sort_values(ascending=False).head(5)
        fig = px.bar(
            x=top_rain.values,
            y=top_rain.index,
            orientation='h',
            title='Top 5 thành phố mưa nhiều nhất',
            labels={'x': 'Tổng lượng mưa (mm)', 'y': 'Thành phố'},
            color=top_rain.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(" Độ Ẩm Theo Mùa")
        df_hum = df_filtered.groupby(['season', 'city'])['humidity'].mean().reset_index()
        fig = px.line_polar(
            df_hum,
            r='humidity',
            theta='season',
            color='city',
            line_close=True,
            title='Độ ẩm trung bình theo mùa (Radar Chart)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ===========================
    # INSIGHTS
    # ===========================
    with st.expander("💡 Insights về mưa"):
        rainiest = df_filtered.groupby('city')['rainfall'].sum().idxmax()
        driest = df_filtered.groupby('city')['rainfall'].sum().idxmin()
        rainiest_season = df_filtered.groupby('season')['rainfall'].sum().idxmax()
        
        st.write(f"🌧️ **Thành phố mưa nhiều nhất:** {rainiest}")
        st.write(f"☀️ **Thành phố ít mưa nhất:** {driest}")
        st.write(f"🍂 **Mùa mưa nhiều nhất:** {rainiest_season}")
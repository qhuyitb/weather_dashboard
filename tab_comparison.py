"""
Tab 6: So Sánh & Tương Quan
"""

import streamlit as st
import pandas as pd
from scipy import stats
from visualizations import (
    create_correlation_heatmap,
    create_radar_chart,
    create_parallel_coordinates,
    create_3d_scatter
)

def render_tab_comparison(df_filtered):
    """Render tab so sánh & tương quan"""
    
    st.header("🔍 So Sánh & Phân Tích Tương Quan")
    
    
    # CORRELATION HEATMAP
    
    st.subheader("📊 Heatmap - Ma Trận Tương Quan")
    
    corr_vars = ['temp_mean', 'temp_max', 'temp_min', 'humidity', 'rainfall', 'temp_range']
    var_labels = {
        'temp_mean': 'Nhiệt độ TB',
        'temp_max': 'Nhiệt độ Max',
        'temp_min': 'Nhiệt độ Min',
        'humidity': 'Độ ẩm',
        'rainfall': 'Lượng mưa',
        'temp_range': 'Chênh lệch nhiệt độ'
    }
    
    # Check if all columns exist
    available_vars = [var for var in corr_vars if var in df_filtered.columns]
    
    if len(available_vars) >= 2:
        # Rename columns để hiển thị tiếng Việt
        df_for_heatmap = df_filtered[available_vars].rename(columns=var_labels)
        fig = create_correlation_heatmap(df_for_heatmap, df_for_heatmap.columns.tolist())
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Không đủ dữ liệu để tạo ma trận tương quan")
    
    
    # COMPARE 2 CITIES
    
    st.subheader(" So Sánh 2 Thành Phố")
    
    selected_cities = df_filtered['city'].unique().tolist()
    
    if len(selected_cities) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            city1 = st.selectbox("Thành phố 1", selected_cities, index=0, key='city1')
        with col2:
            city2 = st.selectbox("Thành phố 2", selected_cities, index=min(1, len(selected_cities)-1), key='city2')
        
        df_city1 = df_filtered[df_filtered['city'] == city1]
        df_city2 = df_filtered[df_filtered['city'] == city2]
        
        # Radar Chart
        fig = create_radar_chart(df_city1, df_city2, city1, city2)
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison Table
        st.subheader(" Bảng So Sánh Chi Tiết")
        
        comparison_data = {
            'Chỉ số': ['Nhiệt độ TB', 'Nhiệt độ Max', 'Nhiệt độ Min', 'Độ ẩm TB', 
                       'Tổng mưa', 'Biên độ nhiệt TB'],
            city1: [
                f"{df_city1['temp_mean'].mean():.1f}°C",
                f"{df_city1['temp_max'].max():.1f}°C",
                f"{df_city1['temp_min'].min():.1f}°C",
                f"{df_city1['humidity'].mean():.0f}%",
                f"{df_city1['rainfall'].sum():.0f}mm",
                f"{df_city1['temp_range'].mean():.1f}°C"
            ],
            city2: [
                f"{df_city2['temp_mean'].mean():.1f}°C",
                f"{df_city2['temp_max'].max():.1f}°C",
                f"{df_city2['temp_min'].min():.1f}°C",
                f"{df_city2['humidity'].mean():.0f}%",
                f"{df_city2['rainfall'].sum():.0f}mm",
                f"{df_city2['temp_range'].mean():.1f}°C"
            ]
        }
        
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
        
        # Statistical Tests
        with st.expander(" Kiểm Định Thống Kê"):
            st.write("### T-test: So sánh nhiệt độ trung bình 2 thành phố")
            
            t_stat, p_value = stats.ttest_ind(
                df_city1['temp_mean'].dropna(),
                df_city2['temp_mean'].dropna()
            )
            
            st.write(f"**T-statistic:** {t_stat:.4f}")
            st.write(f"**P-value:** {p_value:.4f}")
            
            if p_value < 0.05:
                st.success(f"✅ Có sự khác biệt có ý nghĩa thống kê giữa {city1} và {city2}")
            else:
                st.info(f"ℹ️ Không có sự khác biệt có ý nghĩa thống kê giữa {city1} và {city2}")
    
    else:
        st.warning("Cần chọn ít nhất 2 thành phố để so sánh")
    
    
    # PARALLEL COORDINATES
    
    st.subheader(" Parallel Coordinates - So Sánh Đa Chiều")
    
    if len(selected_cities) > 0:
        fig = create_parallel_coordinates(df_filtered)
        st.plotly_chart(fig, use_container_width=True)
    
    
    # 3D SCATTER
    
    st.subheader(" Scatter 3D - Nhiệt Độ × Độ Ẩm × Mưa")
    
    if len(selected_cities) > 0:
        fig = create_3d_scatter(df_filtered)
        st.plotly_chart(fig, use_container_width=True)
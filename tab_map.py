"""
Tab 5: Bản Đồ Tương Tác
"""

import streamlit as st
import folium
from streamlit_folium import folium_static
from visualizations import create_scatter_map

def render_tab_map(df_filtered):
    """Render tab bản đồ"""
    
    st.header("🗺️ Bản Đồ Tương Tác")
    
    # Calculate average by city
    df_map = df_filtered.groupby('city').agg({
        'temp_mean': 'mean',
        'rainfall': 'sum',
        'humidity': 'mean',
        'lat': 'first',
        'lon': 'first'
    }).reset_index()
    
    # PLOTLY SCATTER MAP
    st.subheader(" Bản Đồ Nhiệt Độ Trung Bình")
    
    fig = create_scatter_map(df_map)
    st.plotly_chart(fig, use_container_width=True)
    
    # FOLIUM MAP
    st.subheader(" Bản Đồ Chi Tiết (Folium)")
    
    m = folium.Map(
        location=[16.0, 107.0],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    for _, row in df_map.iterrows():
        # Determine color based on temperature
        if row['temp_mean'] > 28:
            color = 'red'
        elif row['temp_mean'] > 24:
            color = 'orange'
        else:
            color = 'blue'
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['temp_mean'] / 2,
            popup=folium.Popup(f"""
                <div style="font-family: Arial; width: 200px;">
                    <h4 style="color: #667eea;">{row['city']}</h4>
                    <hr style="margin: 5px 0;">
                    <p><b>🌡️ Nhiệt độ TB:</b> {row['temp_mean']:.1f}°C</p>
                    <p><b>💧 Độ ẩm TB:</b> {row['humidity']:.0f}%</p>
                    <p><b>🌧️ Tổng mưa:</b> {row['rainfall']:.0f}mm</p>
                </div>
            """, max_width=250),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6,
            weight=2
        ).add_to(m)
    
    folium_static(m, width=1400, height=600)
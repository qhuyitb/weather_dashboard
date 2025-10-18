"""
Tab 2: Xu Hướng Thời Gian
"""

import streamlit as st
from visualizations import (
    create_line_chart,
    create_area_chart,
    create_seasonal_bar
)

def render_tab_trends(df_filtered):
    """Render tab xu hướng thời gian"""
    
    st.header(" Xu Hướng Theo Thời Gian")
    
    # LINE CHART - Temperature
    st.subheader(" Biểu Đồ Đường - Nhiệt Độ Theo Thời Gian")
    
    fig = create_line_chart(
        df_filtered,
        'date',
        'temp_mean',
        'city',
        'Xu hướng nhiệt độ trung bình'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # AREA CHART - Humidity & Rainfall
    st.subheader(" Biểu Đồ Vùng - Độ Ẩm & Lượng Mưa")
    
    selected_cities = df_filtered['city'].unique().tolist()
    fig = create_area_chart(df_filtered, selected_cities)
    st.plotly_chart(fig, use_container_width=True)
    
    # SEASONAL ANALYSIS
    st.subheader(" Phân Tích Theo Mùa")
    
    fig = create_seasonal_bar(df_filtered)
    st.plotly_chart(fig, use_container_width=True)
    
    # INSIGHTS
    # with st.expander("💡 Phát hiện về xu hướng"):
    #     max_temp_month = df_filtered.groupby('month')['temp_mean'].mean().idxmax()
    #     min_temp_month = df_filtered.groupby('month')['temp_mean'].mean().idxmin()
        
    #     st.write(f"🔥 **Tháng nóng nhất:** Tháng {max_temp_month}")
    #     st.write(f"❄️ **Tháng lạnh nhất:** Tháng {min_temp_month}")
    #     # st.write("📊 **Xu hướng:** Nhiệt độ tăng dần từ tháng 3-8, giảm từ tháng 9-12")
    
    # INSIGHTS
    with st.expander("💡 Phát hiện về xu hướng"):
        # Tính toán động theo tháng
        monthly_temp = df_filtered.groupby('month')['temp_mean'].mean()
        max_temp_month = int(monthly_temp.idxmax())
        min_temp_month = int(monthly_temp.idxmin())
        
        # Tìm xu hướng tăng/giảm
        temp_sorted = monthly_temp.sort_index()
        peak_month = int(temp_sorted.idxmax())
        
        # Tìm tháng bắt đầu xu hướng tăng (tháng lạnh nhất)
        months_before_peak = temp_sorted[:peak_month]
        if len(months_before_peak) > 0:
            increasing_start = int(months_before_peak.idxmin())
        else:
            increasing_start = int(temp_sorted.index[0])
        
        # Tháng kết thúc (tháng cuối trong data)
        end_month = int(temp_sorted.index[-1])
        
        st.write(f"🔥 **Tháng nóng nhất:** Tháng {max_temp_month}")
        st.write(f"❄️ **Tháng lạnh nhất:** Tháng {min_temp_month}")
        st.write(f"📊 **Xu hướng:** Nhiệt độ tăng dần từ tháng {increasing_start}-{peak_month}, giảm từ tháng {peak_month}-{end_month}")
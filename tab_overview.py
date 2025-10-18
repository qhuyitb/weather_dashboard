"""
Tab 1: Tổng Quan & Thống Kê
"""
import networkx as nx
import streamlit as st
from data_fetcher import get_statistics
from visualizations import (
    create_histogram, 
    create_boxplot, 
    create_violin_plot,
    # create_wordcloud,
    create_network_graph
)

def render_tab_overview(df_filtered):
    """Render tab tổng quan"""
    
    st.header("📊 Thống Kê Tổng Quan")
    
    # KPI METRICS
    stats = get_statistics(df_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌡️ Nhiệt độ TB", 
            f"{stats.get('avg_temp', 0):.1f}°C"
        )
    
    with col2:
        st.metric(
            "💧 Độ ẩm TB", 
            f"{stats.get('avg_humidity', 0):.0f}%"
        )
    
    with col3:
        st.metric(
            "🌧️ Tổng lượng mưa", 
            f"{stats.get('total_rainfall', 0):.0f}mm"
        )
    
    with col4:
        st.metric(
            "🔥 Nhiệt độ cao nhất", 
            f"{stats.get('max_temp', 0):.1f}°C"
        )
    
    st.markdown("---")
    
    # CHARTS
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Histogram - Phân Bố Nhiệt Độ")
        fig = create_histogram(
            df_filtered, 
            'temp_mean',
            'Phân bố nhiệt độ trung bình',
            'Nhiệt độ (°C)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(" Boxplot - Nhiệt Độ Theo Thành Phố")
        fig = create_boxplot(
            df_filtered,
            'city',
            'temp_mean',
            'So sánh nhiệt độ các thành phố'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Violin Plot
    st.subheader(" Violin Plot - Phân Bố Chi Tiết")
    fig = create_violin_plot(
        df_filtered,
        'city',
        'temp_mean',
        'Phân bố nhiệt độ chi tiết (Violin Plot)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # NETWORK GRAPH
    st.subheader(" Network Graph - Mối Liên Hệ Thời Tiết")
    fig_net = create_network_graph(df_filtered)
    if fig_net:
        st.plotly_chart(fig_net, use_container_width=True)
    
    
    # WordCloud
    # st.subheader("☁️ WordCloud - Đặc Điểm Thời Tiết")
    # fig = create_wordcloud(df_filtered)
    # st.pyplot(fig)
    
    # INSIGHTS
    with st.expander("💡 Phát hiện thú vị"):
        st.write(f"🔥 **Thành phố nóng nhất:** {stats.get('hottest_city', 'N/A')}")
        st.write(f"❄️ **Thành phố mát nhất:** {stats.get('coldest_city', 'N/A')}")
        st.write(f"🌧️ **Thành phố mưa nhiều nhất:** {stats.get('rainiest_city', 'N/A')}")
        st.write(f"☀️ **Thành phố ít mưa nhất:** {stats.get('driest_city', 'N/A')}")
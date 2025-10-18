"""
Module chứa các hàm tạo biểu đồ
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx

# COLORS
COLOR_PALETTE = px.colors.qualitative.Set2

# BASIC CHARTS
def create_histogram(df, column, title, x_label, nbins=30):
    """Tạo histogram"""
    fig = px.histogram(
        df, 
        x=column,
        nbins=nbins,
        title=title,
        labels={column: x_label, 'count': 'Tần suất'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_boxplot(df, x_col, y_col, title, color_col=None):
    """Tạo boxplot"""
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=color_col or x_col,
        title=title,
        labels={y_col: 'Giá trị', x_col: 'Nhóm'}
    )
    fig.update_layout(height=400)
    return fig

def create_violin_plot(df, x_col, y_col, title):
    """Tạo violin plot"""
    fig = px.violin(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        box=True,
        points='outliers',
        title=title,
        labels={y_col: 'Giá trị', x_col: 'Nhóm'}
    )
    fig.update_layout(height=450)
    return fig

# TIME SERIES CHARTS
def create_line_chart(df, x_col, y_col, color_col, title):
    """Tạo line chart"""
    df_grouped = df.groupby([x_col, color_col])[y_col].mean().reset_index()
    
    fig = px.line(
        df_grouped,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: 'Thời gian', y_col: 'Giá trị'}
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(height=450, hovermode='x unified')
    return fig

def create_area_chart(df, cities):
    """Tạo area chart cho độ ẩm và mưa"""
    df_monthly = df.groupby(['month', 'city']).agg({
        'humidity': 'mean',
        'rainfall': 'sum'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    for city in cities:
        city_data = df_monthly[df_monthly['city'] == city]
        
        # Độ ẩm (trục trái)
        fig.add_trace(
            go.Scatter(
                x=city_data['month'],
                y=city_data['humidity'],
                name=f'{city} - Độ ẩm',
                fill='tonexty',
                mode='lines'
            ),
            secondary_y=False
        )
        
        # Mưa (trục phải)
        fig.add_trace(
            go.Bar(
                x=city_data['month'],
                y=city_data['rainfall'],
                name=f'{city} - Mưa',
                opacity=0.6
            ),
            secondary_y=True
        )
    
    fig.update_xaxes(title_text="Tháng")
    fig.update_yaxes(title_text="Độ ẩm (%)", secondary_y=False)
    fig.update_yaxes(title_text="Lượng mưa (mm)", secondary_y=True)
    fig.update_layout(
        title='Xu hướng độ ẩm và lượng mưa theo tháng',
        height=450,
        hovermode='x unified'
    )
    
    return fig

# SCATTER & CORRELATION
def create_scatter_with_regression(df, x_col, y_col, color_col, size_col=None):
    """Tạo scatter plot với đường hồi quy"""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        trendline='ols',
        title=f'Mối quan hệ {x_col} - {y_col}',
        labels={x_col: x_col, y_col: y_col}
    )
    fig.update_layout(height=450)
    return fig

def create_correlation_heatmap(df, columns):
    """Tạo heatmap tương quan"""
    corr_matrix = df[columns].corr()
    
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Hệ số tương quan"),
        x=columns,
        y=columns,
        color_continuous_scale='RdBu',
        zmin=-1, zmax=1,
        title='Ma trận tương quan',
        text_auto='.2f'
    )
    fig.update_layout(height=500)
    return fig

# HIERARCHICAL CHARTS
def create_treemap(df, path_cols, value_col, title):
    """Tạo treemap"""
    df_grouped = df.groupby(path_cols)[value_col].sum().reset_index()
    
    fig = px.treemap(
        df_grouped,
        path=[px.Constant("Việt Nam")] + path_cols,
        values=value_col,
        title=title,
        color=value_col,
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=500)
    return fig

def create_sunburst(df):
    """Tạo sunburst chart cho mưa"""
    df_sun = df.groupby(['region', 'season', 'city'])['rainfall'].sum().reset_index()
    
    fig = px.sunburst(
        df_sun,
        path=['region', 'season', 'city'],
        values='rainfall',
        title='Phân bố lượng mưa theo vùng → mùa → thành phố',
        color='rainfall',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=600)
    return fig

# MAPS
def create_scatter_map(df_map):
    """Tạo scatter mapbox"""
    fig = px.scatter_mapbox(
        df_map,
        lat='lat',
        lon='lon',
        size='temp_mean',
        color='temp_mean',
        hover_name='city',
        hover_data={
            'temp_mean': ':.1f', 
            'rainfall': ':.0f', 
            'humidity': ':.0f',
            'lat': False, 
            'lon': False
        },
        size_max=30,
        zoom=5,
        mapbox_style='open-street-map',
        title='Nhiệt độ trung bình các thành phố',
        color_continuous_scale='RdYlBu_r',
        labels={
            'temp_mean': 'Nhiệt độ (°C)', 
            'rainfall': 'Mưa (mm)', 
            'humidity': 'Độ ẩm (%)'
        }
    )
    fig.update_layout(height=600)
    return fig

# COMPARISON CHARTS
def create_radar_chart(city1_data, city2_data, city1_name, city2_name):
    """Tạo radar chart so sánh 2 thành phố"""
    categories = ['Nhiệt độ TB', 'Độ ẩm', 'Lượng mưa', 'Biên độ nhiệt']
    
    city1_values = [
        city1_data['temp_mean'].mean() / 35 * 100,
        city1_data['humidity'].mean(),
        city1_data['rainfall'].mean() * 2,
        city1_data['temp_range'].mean() * 10
    ]
    
    city2_values = [
        city2_data['temp_mean'].mean() / 35 * 100,
        city2_data['humidity'].mean(),
        city2_data['rainfall'].mean() * 2,
        city2_data['temp_range'].mean() * 10
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=city1_values,
        theta=categories,
        fill='toself',
        name=city1_name
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=city2_values,
        theta=categories,
        fill='toself',
        name=city2_name
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f'So sánh profile khí hậu: {city1_name} vs {city2_name}',
        height=450
    )
    
    return fig

def create_parallel_coordinates(df):
    """Tạo parallel coordinates"""
    df_parallel = df.groupby('city').agg({
        'temp_mean': 'mean',
        'humidity': 'mean',
        'rainfall': 'sum',
        'temp_range': 'mean'
    }).reset_index()
    
    fig = px.parallel_coordinates(
        df_parallel,
        dimensions=['temp_mean', 'humidity', 'rainfall', 'temp_range'],
        color='temp_mean',
        labels={
            'temp_mean': 'Nhiệt độ TB',
            'humidity': 'Độ ẩm',
            'rainfall': 'Mưa',
            'temp_range': 'Biên độ'
        },
        color_continuous_scale='Viridis',
        title='So sánh đa chiều các thành phố'
    )
    fig.update_layout(height=450)
    return fig

def create_3d_scatter(df):
    """Tạo 3D scatter plot"""
    df_3d = df.groupby('city').agg({
        'temp_mean': 'mean',
        'humidity': 'mean',
        'rainfall': 'sum'
    }).reset_index()
    
    fig = px.scatter_3d(
        df_3d,
        x='temp_mean',
        y='humidity',
        z='rainfall',
        color='city',
        size='rainfall',
        title='Phân tích 3D: Nhiệt độ - Độ ẩm - Lượng mưa',
        labels={
            'temp_mean': 'Nhiệt độ (°C)',
            'humidity': 'Độ ẩm (%)',
            'rainfall': 'Mưa (mm)'
        },
        size_max=30
    )
    fig.update_layout(height=700)
    return fig

# SPECIAL CHARTS
def create_heatmap_calendar(df, city):
    """Tạo heatmap calendar"""
    df_city = df[df['city'] == city].copy()
    df_city['week'] = df_city['date'].dt.isocalendar().week
    df_city['dayofweek'] = df_city['date'].dt.dayofweek
    
    pivot = df_city.pivot_table(
        values='temp_mean',
        index='week',
        columns='dayofweek',
        aggfunc='mean'
    )
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Ngày trong tuần", y="Tuần", color="Nhiệt độ (°C)"),
        x=['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'],
        title=f'Nhiệt độ theo lịch - {city}',
        color_continuous_scale='RdYlBu_r'
    )
    fig.update_layout(height=500)
    return fig

# def create_wordcloud(df):
#     """Tạo WordCloud"""
#     weather_text = []
#     for _, row in df.iterrows():
#         weather_text.append(f"{row['city']} ")
#         weather_text.append(f"{row['season']} ")
#         weather_text.append(f"{row['temp_category']} ")
#         weather_text.append(f"{row['rain_category']} ")
    
#     text = ' '.join(weather_text)
    
#     wordcloud = WordCloud(
#         width=800, 
#         height=400,
#         background_color='white',
#         colormap='viridis',
#         relative_scaling=0.5,
#         min_font_size=10
#     ).generate(text)
    
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.imshow(wordcloud, interpolation='bilinear')
#     ax.axis('off')
    
#     return fig

def create_network_graph(df):
    """Tạo Network Graph thể hiện mối liên hệ"""
    
    if df.empty:
        return None
    
    # Tạo graph
    G = nx.Graph()
    
    # Thêm nodes cho thành phố
    for city in df['city'].unique():
        G.add_node(city, node_type='city')
    
    # Thêm nodes cho mùa
    for season in df['season'].unique():
        G.add_node(season, node_type='season')
    
    # Thêm edges - kết nối thành phố với mùa
    city_season_pairs = df[['city', 'season']].drop_duplicates()
    for _, row in city_season_pairs.iterrows():
        G.add_edge(row['city'], row['season'], weight=2)
    
    # Tính layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Chuẩn bị dữ liệu cho Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        showlegend=False
    )
    
    # Nodes
    node_x = []
    node_y = []
    node_color = []
    node_size = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Màu và kích thước theo loại
        if G.nodes[node].get('node_type') == 'city':
            node_color.append('#FF6B6B')  # Đỏ cho thành phố
            node_size.append(25)
            node_text.append(f"<b>{node}</b><br>Thành phố")
        else:
            node_color.append('#4ECDC4')  # Xanh cho mùa
            node_size.append(20)
            node_text.append(f"<b>{node}</b><br>Mùa")
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hovertext=node_text,
        hoverinfo='text',
        marker=dict(
            size=node_size,
            color=node_color,
            line_width=2,
            line_color='white'
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title='Network - Mối Liên Hệ Thành Phố & Mùa',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#f8f9fa',
        height=600
    )
    
    return fig

def create_seasonal_bar(df):
    """Tạo bar chart theo mùa"""
    df_season = df.groupby(['season', 'city'])['temp_mean'].mean().reset_index()
    
    fig = px.bar(
        df_season,
        x='season',
        y='temp_mean',
        color='city',
        barmode='group',
        title='Nhiệt độ trung bình theo mùa',
        labels={'season': 'Mùa', 'temp_mean': 'Nhiệt độ (°C)', 'city': 'Thành phố'}
    )
    fig.update_layout(height=450)
    return fig
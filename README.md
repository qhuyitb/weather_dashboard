# 🌤️ Dashboard Phân Tích Thời Tiết Việt Nam 2025

Dashboard tương tác phân tích dữ liệu thời tiết thực tế từ 8 thành phố lớn Việt Nam trong năm 2025.

## 📋 Tính Năng

###  Đáp ứng đầy đủ yêu cầu:

-  **Thu thập dữ liệu:** Open-Meteo API (không cần API key)
-  **Chuẩn hóa & Feature Engineering:** Xử lý missing data, tạo các cột mới
-  **Histogram/Boxplot/Violin:** Tab 1
-  **Network Graph:** Tab 1 - Mối Liên Hệ Thời Tiết
-  **Line/Area Chart:** Tab 2 - Xu hướng thời gian
-  **Scatter + Regression:** Tab 3 - Phân tích nhiệt độ
-  **Treemap/Sunburst:** Tab 4 - Phân tích mưa
-  **Heatmap Correlation:** Tab 5 - Ma trận tương quan
-  **Bản đồ tương tác:** Tab 6 - Folium & Plotly Map

-  **15+ biểu đồ tương tác:** Tất cả dùng Plotly

## 🚀 Cài Đặt & Chạy

### Bước 1: Clone/Tải project

```bash
# Tạo thư mục project
mkdir weather-dashboard
cd weather-dashboard
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng

```bash
streamlit run app.py
```

Dashboard sẽ mở tự động tại: `http://localhost:8501`

## 📊 Cấu Trúc Dashboard

### Tab 1: 📊 Tổng Quan & Thống Kê
- KPI Cards (4 chỉ số quan trọng)
- Histogram phân bố nhiệt độ
- Boxplot so sánh thành phố
- Violin plot phân bố chi tiết
- Network Graph Mối Liên Hệ Thời Tiết

### Tab 2: 📈 Xu Hướng Thời Gian
- Line chart nhiệt độ theo thời gian
- Area chart độ ẩm & mưa
- Phân tích theo mùa
- Insights tự động

### Tab 3: 🌡️ Phân Tích Nhiệt Độ
- Scatter plot với hồi quy tuyến tính
- Heatmap calendar nhiệt độ
- Phân tích biên độ nhiệt
- Correlation coefficient

### Tab 4: 💧 Phân Tích Độ Ẩm & Mưa
- Treemap tổng lượng mưa
- Sunburst phân bố theo mùa
- Top thành phố mưa nhiều
- Radar chart độ ẩm
  
### Tab 5: 🔍 So Sánh & Tương Quan
- Heatmap correlation matrix
- Radar chart so sánh 2 thành phố
- Parallel coordinates
- Scatter 3D
- T-test thống kê

### Tab 6: 🗺️ Bản Đồ Tương Tác
- Plotly scatter map
- Folium detailed map với markers
- Visualize không gian địa lý



## 🎛️ Tính Năng Tương Tác

- ✅ **Multiselect:** Chọn nhiều thành phố
- ✅ **Date range:** Lọc theo khoảng thời gian
- ✅ **Season filter:** Chọn mùa cụ thể
- ✅ **City comparison:** So sánh 2 thành phố
- ✅ **Download CSV:** Export dữ liệu đã lọc
- ✅ **Hover tooltips:** Chi tiết khi rê chuột
- ✅ **Zoom/Pan:** Phóng to thu nhỏ biểu đồ

## 🌍 Nguồn Dữ Liệu

**Open-Meteo Archive API** (Free, không cần đăng ký):
- URL: `https://archive-api.open-meteo.com/v1/archive`
- Variables: nhiệt độ max/min/mean, độ ẩm, lượng mưa
- Time range: 01/01/2025 - today(<=31/12/2025)
- 8 thành phố: Hà Nội, HCM, Đà Nẵng, Hải Phòng, Cần Thơ, Huế, Nha Trang, Vũng Tàu

## 📈 Feature Engineering

```python
# Các cột được tạo thêm:
- month, day: Tháng, ngày
- season: Mùa (Xuân/Hè/Thu/Đông)
- temp_range: Biên độ nhiệt (max - min)
- temp_category: Phân loại (Mát/Ấm/Nóng)
- humidity_level: Mức độ ẩm (Thấp/TB/Cao)
- rain_category: Mức độ mưa (Ít/Vừa/Nhiều)
- region: Vùng miền (Bắc/Trung/Nam)
```

## 🎨 Công Nghệ Sử Dụng

- **Streamlit:** Framework web app
- **Plotly:** Biểu đồ tương tác
- **Folium:** Bản đồ địa lý
- **Pandas/Numpy:** Xử lý dữ liệu
- **Scipy:** Thống kê & correlation
- **WordCloud:** Visualization text
- **Requests:** API calls
- **BeautifulSoup:** Backup crawling (nếu cần)

## 📱 Deploy Lên Cloud

### Option 1: Streamlit Community Cloud (Miễn phí)

1. Push code lên GitHub
2. Truy cập https://share.streamlit.io
3. Connect repository
4. Deploy!

### Option 2: Chạy local

```bash
streamlit run app.py --server.port 8501
```

## 💡 Insights Tự Động

Dashboard tự động tính toán và hiển thị:
- ✅ Thành phố nóng/lạnh nhất
- ✅ Thành phố mưa nhiều/ít nhất
- ✅ Tháng có nhiệt độ cực trị
- ✅ Tương quan nhiệt độ - độ ẩm
- ✅ Kiểm định thống kê (T-test)
- ✅ Xu hướng theo mùa

## 📝 Lưu Ý

- **Cache data:** Dữ liệu được cache 1 giờ để tăng tốc độ
- **Rate limit:** API có thể giới hạn requests, nên cache
- **Responsive:** Tự động điều chỉnh theo màn hình
- **Export:** Có thể tải CSV và in PDF (Ctrl+P)

## 🔧 Customize

Muốn thêm thành phố khác? Sửa trong `CITIES`:

```python
CITIES = {
    'Tên Thành Phố': {'lat': x.xxxx, 'lon': y.yyyy, 'region': 'Bắc/Trung/Nam'}
}
```

## 📞 Hỗ Trợ

Nếu gặp lỗi:
1. Kiểm tra kết nối internet (cần để gọi API)
2. Cài đúng dependencies: `pip install -r requirements.txt`
3. Đảm bảo Python >= 3.8

## 📄 License

MIT License - Tự do sử dụng cho học tập và nghiên cứu

---

**Made with ❤️ by Quang Huy for Data Visualization**

🌟 Nếu thích project, đừng quên star trên GitHub!

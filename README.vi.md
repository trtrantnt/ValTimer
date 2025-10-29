# ⏱️ ValTimer - Bộ Đếm Spike Valorant

<div align="center">

![Valorant](https://img.shields.io/badge/Valorant-Spike%20Timer-ff4655?style=for-the-badge&logo=valorant&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Phát hiện Spike tự động và hiển thị bộ đếm thời gian overlay cho Valorant**

[Tải Phiên Bản Mới Nhất](https://github.com/trtrantnt/ValTimer/releases) • [Báo Lỗi](https://github.com/trtrantnt/ValTimer/issues) • [Yêu Cầu Tính Năng](https://github.com/trtrantnt/ValTimer/issues)

</div>

---

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Ảnh Chụp Màn Hình](#-ảnh-chụp-màn-hình)
- [Cài Đặt](#-cài-đặt)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Build Từ Source](#-build-từ-source)
- [Công Nghệ](#-công-nghệ)
- [Câu Hỏi Thường Gặp](#-câu-hỏi-thường-gặp)
- [Đóng Góp](#-đóng-góp)
- [Giấy Phép](#-giấy-phép)

---

## 🎯 Giới Thiệu

**ValTimer** là ứng dụng overlay thông minh tự động phát hiện khi Spike được cài trong Valorant và hiển thị bộ đếm thời gian chính xác 45 giây. Được xây dựng với computer vision (OpenCV), nó sử dụng template matching để phát hiện biểu tượng Spike trên màn hình của bạn.

Hoàn hảo cho:
- 🎮 Người chơi thi đấu cần thời gian chính xác
- 📊 Người chơi đang học timing và rotation của Spike
- 🏆 Đội nhóm phối hợp chiến thuật dỡ bom/phản công

---

## ✨ Tính Năng

### 🌐 **Hỗ Trợ Song Ngữ (MỚI trong v1.3.0)**
- **Tiếng Việt/Tiếng Anh** - Chuyển đổi ngôn ngữ đầy đủ
- **Nút Chuyển EN/VI** - Đổi ngôn ngữ ngay lập tức
- Tất cả thành phần UI được dịch (nút, nhãn, bảng thông tin, cảnh báo)
- Chuyển đổi ngôn ngữ liền mạch không cần khởi động lại

### 🔍 **Phát Hiện Tự Động**
- Phát hiện cài Spike thời gian thực bằng OpenCV template matching
- **Phát hiện kết thúc vòng thông minh** - tự động dừng đếm khi vòng kết thúc
- Không cần sửa đổi game hay đọc bộ nhớ
- Hoạt động hoàn toàn qua chụp màn hình (an toàn & không thể phát hiện)

### ⏰ **Bộ Đếm Chính Xác**
- Bộ đếm 45 giây overlay xuất hiện tự động
- **Màu Sắc Theo Thời Gian**:
  - 🟦 Cyan (45s-21s): Thời gian an toàn
  - 🟨 Vàng (20s-11s): Cảnh báo
  - 🟧 Cam (10s-8s): Nguy hiểm
  - 🟥 Đỏ (<7s): Cực kỳ nguy hiểm với hiển thị số thập phân
- **Cập Nhật Vị Trí Trực Tiếp** - Đổi vị trí overlay khi đang chạy (không cần khởi động lại)
- **4 Vị Trí Góc** - Trên-trái, trên-phải, dưới-trái, dưới-phải
- **Tự động dừng khi vòng kết thúc** - phát hiện khi biểu tượng Spike biến mất
- Thời gian chờ 50 giây giữa các lần phát hiện để tránh kích hoạt sai

### 🖥️ **Hỗ Trợ Đa Độ Phân Giải**
- **1920x1080** (Full HD) - Tất cả 4 góc
- **2560x1440** (2K/1440p) - Tất cả 4 góc
- **1440x1080** (4:3 stretched) - Tất cả 4 góc
- ROI (Region of Interest) được tối ưu cho mỗi độ phân giải

### 🎨 **Giao Diện Hiện Đại**
- **Giao Diện Chủ Đề Valorant** với thiết kế card hiện đại
- **Bảng Thông Tin Có Thể Thu Gọn** - Bảng Thông Tin Spike và Về Tác Giả mở rộng inline
- **Bố Cục Nút Cải Thiện** - 3 nút căn giữa với kích thước tối ưu:
  - Thông Tin Spike (Xanh dương): Cơ chế và timing của Spike
  - Về Tác Giả (Xanh dương): Thông tin ứng dụng
  - EN/VI (Xanh lá): Chuyển đổi ngôn ngữ
- **Tích Hợp System Tray** - Thu nhỏ vào khay hệ thống
- **Nút EXIT** - Thoát nhanh từ cửa sổ chính

### 📊 **Bảng Thông Tin**
- **Bảng Thông Tin Spike**: Chi tiết cơ chế Spike (thời gian cài, nổ, dỡ)
- **Bảng Giới Thiệu**: Phiên bản ứng dụng, thông tin nhà phát triển, link GitHub
- **Loại Trừ Lẫn Nhau**: Mở bảng này sẽ đóng bảng kia
- **Cảnh Báo Windowed Fullscreen**: Cảnh báo màu cam rõ ràng cho yêu cầu chế độ game

### ⚡ **Tối Ưu Hiệu Suất**
- **Giảm 90% CPU** trong khi đếm (20 FPS → ~1.67 FPS hiệu quả)
- Tốc độ quét thích ứng: 20 FPS khi phát hiện, 5 FPS với bỏ qua khung hình khi đếm
- Quản lý tài nguyên thông minh cho phiên chơi game dài
- Xem [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) để biết chi tiết

---

## 📸 Ảnh Chụp Màn Hình

### Giao Diện Chính - Tiếng Anh

![Giao Diện Tiếng Việt ValTimer](https://raw.githubusercontent.com/trtrantnt/ValTimer/main/p2.png)

### Overlay góc dưới-trái trong game

![Giao Diện Chính ValTimer](https://raw.githubusercontent.com/trtrantnt/ValTimer/main/p1.png)

---

## 📥 Cài Đặt

### Tùy Chọn 1: Tải File Thực Thi (Khuyên Dùng)

1. Vào [Releases](https://github.com/trtrantnt/ValTimer/releases)
2. Tải `ValTimer.exe` phiên bản mới nhất
3. Chạy file thực thi (không cần cài đặt!)

### Tùy Chọn 2: Chạy Từ Source

```bash
# Clone repository
git clone https://github.com/trtrantnt/ValTimer.git
cd ValTimer

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python timer_valo.py
```

---

## 🚀 Hướng Dẫn Sử Dụng

### Bắt Đầu Nhanh

1. **Khởi chạy ValTimer.exe**
2. **Chọn độ phân giải** (1920x1080, 2560x1440, hoặc 1440x1080)
3. **Click "Start Detection"**
4. **Chơi Valorant!**
   - Bộ đếm sẽ tự động xuất hiện khi Spike được cài
   - Bộ đếm hiển thị đếm ngược chính xác từ 45 giây

### Các Nút Điều Khiển

| Nút | Mô Tả |
|-----|-------|
| **1920x1080** | Chọn độ phân giải Full HD |
| **2560x1440** | Chọn độ phân giải 2K/1440p |
| **1440x1080** | Chọn độ phân giải 4:3 stretched |
| **Trên-Trái/Phải/Dưới-Trái/Phải** | Chọn vị trí overlay đếm ngược |
| **Thông Tin Spike / Spike Info** | Xem cơ chế và timing của Spike |
| **Về Tác Giả / About Me** | Xem thông tin ứng dụng |
| **EN/VI** | Chuyển đổi giữa Tiếng Anh và Tiếng Việt |
| **❌ EXIT** | Thoát ứng dụng |
| **⏹ DỪNG BỘ ĐẾM** | Dừng phát hiện và ẩn bộ đếm |

### Chuyển Đổi Ngôn Ngữ

- Click nút **🌐 EN/VI** để chuyển đổi giữa Tiếng Việt và Tiếng Anh
- Tất cả thành phần UI cập nhật ngay lập tức
- Ngôn ngữ được lưu giữa các phiên
- **Tiếng Việt**: Dịch đầy đủ bao gồm nút, nhãn và bảng thông tin
- **Tiếng Anh**: Giao diện Tiếng Anh gốc

### Vị Trí Bộ Đếm

- **Đổi vị trí bất cứ lúc nào** - ngay cả khi bộ đếm đang chạy!
- Chọn từ 4 vị trí góc cho mỗi độ phân giải
- Không cần khởi động lại phát hiện
- Vị trí cập nhật ngay lập tức trên màn hình

### System Tray

- **Thu nhỏ**: Click ❌ để thu nhỏ vào khay hệ thống
- **Hiện Cửa Sổ**: Click phải vào biểu tượng khay → Show
- **Thoát**: Click phải vào biểu tượng khay → Exit

### Tìm ROI Cho Độ Phân Giải Tùy Chỉnh

Nếu độ phân giải của bạn không được hỗ trợ, sử dụng `find_spike_position.py` để tìm ROI đúng:

```bash
# 1. Chạy công cụ tìm ROI
python find_spike_position.py

# 2. Vào Valorant và cài Spike
# 3. Alt+Tab về và nhấn Enter để chụp màn hình
# 4. Vẽ hình chữ nhật xung quanh biểu tượng Spike
# 5. Nhấn 's' để lưu tọa độ ROI

# 6. Copy output vào timer_valo.py RESOLUTION_SETTINGS
```

Công cụ sẽ tạo:
- ✅ Tọa độ ROI ở định dạng Python
- ✅ File JSON với dữ liệu ROI
- ✅ Ảnh chụp màn hình và ảnh vùng ROI

---

## 🔨 Build Từ Source

### Yêu Cầu

- Python 3.13 trở lên
- pip package manager

### Các Bước Build

```bash
# 1. Clone repository
git clone https://github.com/trtrantnt/ValTimer.git
cd ValTimer

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Build executable
python -m PyInstaller --onefile --windowed --name "ValTimer" timer_valo.py

# 4. Tìm executable trong thư mục dist/
cd dist
```

---

## 🛠️ Công Nghệ

- **Python 3.13** - Ngôn ngữ lập trình cốt lõi
- **OpenCV (cv2)** - Computer vision và template matching
- **NumPy** - Tính toán số cho xử lý ảnh
- **MSS** - Chụp màn hình nhanh
- **Tkinter** - Framework GUI
- **Pillow (PIL)** - Xử lý hình ảnh
- **pystray** - Tích hợp system tray
- **PyInstaller** - Đóng gói executable

### Thuật Toán Phát Hiện

1. **Chụp Màn Hình**: Chụp ROI bằng MSS (cực nhanh)
2. **Phát Hiện Cạnh**: Áp dụng Canny edge detection (ngưỡng: 100, 200)
3. **Template Matching**: Sử dụng phương pháp `TM_CCOEFF_NORMED`
4. **Ngưỡng**: Độ tin cậy khớp > 0.15 kích hoạt đếm ngược
5. **Phát Hiện Kết Thúc Vòng**: Giám sát biểu tượng Spike biến mất (10 khung hình liên tiếp < ngưỡng 0.05)
6. **Thời Gian Chờ**: Thời gian chờ 50 giây ngăn phát hiện trùng lặp

### Tính Năng Hiệu Suất

- **Tốc Độ Quét Thích Ứng**: Tự động giảm từ 20 FPS xuống 5 FPS trong khi đếm
- **Bỏ Qua Khung Hình**: Chỉ xử lý 1 trong 3 khung hình khi đếm (~1.67 FPS hiệu quả)
- **Phát Hiện Thông Minh**: Dừng đếm khi vòng kết thúc (Spike nổ/được dỡ)
- **Tiết Kiệm Tài Nguyên**: Giảm 90% sử dụng CPU trong khi đếm hoạt động

---

## ❓ Câu Hỏi Thường Gặp

### **H: Sử dụng này có an toàn không? Tôi có bị cấm không?**

Đ: ValTimer chỉ sử dụng chụp màn hình - nó không sửa đổi file game hay đọc bộ nhớ game. Nó hoàn toàn bên ngoài và không thể phát hiện.

### **H: Tại sao phát hiện không hoạt động?**

Đ: Đảm bảo bạn đã chọn độ phân giải đúng khớp với cài đặt hiển thị Valorant của bạn. Cũng đảm bảo Valorant ở chế độ **Windowed Fullscreen** (không phải Fullscreen).

### **H: Tôi có thể thay đổi ngôn ngữ không?**

Đ: Có! Click nút **🌐 EN/VI** để chuyển đổi giữa Tiếng Việt và Tiếng Anh. Tất cả văn bản cập nhật ngay lập tức.

### **H: Tôi có thể di chuyển bộ đếm khi nó đang chạy không?**

Đ: Có! Chọn bất kỳ vị trí góc nào trong 4 vị trí và bộ đếm sẽ di chuyển ngay lập tức mà không cần khởi động lại phát hiện.

### **H: Các màu của bộ đếm có ý nghĩa gì?**

Đ:
- **Cyan (45s-21s)**: Thời gian an toàn - còn nhiều thời gian
- **Vàng (20s-11s)**: Cảnh báo - cân nhắc vị trí của bạn
- **Cam (10s-8s)**: Nguy hiểm - đến lúc quyết định
- **Đỏ (<7s)**: Cực kỳ nguy hiểm - hiển thị số thập phân cho timing chính xác

### **H: Tôi có thể sử dụng với độ phân giải khác không?**

Đ: Hiện tại chỉ hỗ trợ 1080p, 1440p, và 4:3 (1440x1080). Gửi issue để yêu cầu độ phân giải của bạn!

### **H: Điều này có hoạt động với Vanguard anti-cheat không?**

Đ: Có! ValTimer chạy hoàn toàn bên ngoài game và không tương tác với process của Valorant.

### **H: Bộ đếm xuất hiện vào thời điểm sai**

Đ: Thử điều chỉnh ngưỡng phát hiện hoặc đảm bảo độ phân giải thích hợp được chọn. Chế độ debug có thể giúp hiển thị ROI.

### **H: Làm thế nào để bật chế độ debug?**

Đ: Mở `timer_valo.py`, đổi `DEBUG_MODE = False` thành `DEBUG_MODE = True`, và build lại.

### **H: Bộ đếm có dừng khi vòng kết thúc không?**

Đ: Có! Bộ đếm tự động phát hiện khi biểu tượng Spike biến mất (vòng kết thúc) và dừng đếm ngược ngay lập tức.

### **H: Điều này có làm chậm game của tôi không?**

Đ: Không! ValTimer sử dụng tốc độ quét thích ứng và bỏ qua khung hình để giảm thiểu sử dụng CPU (chỉ ~1.67 FPS khi đếm), đảm bảo không ảnh hưởng đến hiệu suất game.

### **H: Sự khác biệt giữa bảng Info và About là gì?**

Đ: **Thông Tin Spike** hiển thị cơ chế game (thời gian cài/dỡ), trong khi **Về Tác Giả** hiển thị thông tin ứng dụng (phiên bản, nhà phát triển, GitHub).

---

## 🤝 Đóng Góp

Chào mừng các đóng góp! Đây là cách bạn có thể giúp đỡ:

1. 🐛 **Báo Lỗi**: [Gửi issue](https://github.com/trtrantnt/ValTimer/issues)
2. 💡 **Yêu Cầu Tính Năng**: [Mở yêu cầu tính năng](https://github.com/trtrantnt/ValTimer/issues)
3. 🔧 **Gửi Pull Request**:
   ```bash
   # Fork repo
   # Tạo feature branch
   git checkout -b feature/TinhNangTuyetVoi
   
   # Commit thay đổi
   git commit -m 'Thêm TinhNangTuyetVoi'
   
   # Push lên branch
   git push origin feature/TinhNangTuyetVoi
   
   # Mở Pull Request
   ```

---

## 📄 Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem file [LICENSE](LICENSE) để biết chi tiết.

---

## 🙏 Lời Cảm Ơn

- Riot Games vì đã tạo ra Valorant
- Cộng đồng OpenCV cho công cụ computer vision
- Tất cả những người đóng góp và người dùng ValTimer

---

<div align="center">

**⭐ Nếu bạn thấy dự án này hữu ích, hãy cân nhắc cho nó một ngôi sao!**

[⬆ Về Đầu Trang](#️-valtimer---bộ-đếm-spike-valorant)

</div>

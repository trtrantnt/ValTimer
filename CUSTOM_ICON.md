# Hướng dẫn tùy chỉnh icon cho ValTimer

## Cách tạo icon mới

### Bước 1: Chỉnh sửa app_icon.py
Mở file `app_icon.py` và tùy chỉnh:

```python
# Thay đổi màu sắc
BACKGROUND_COLOR = '#ff4655'  # Màu nền (hex)
TEXT_COLOR = 'white'          # Màu chữ
ICON_TEXT = 'V'               # Chữ hiển thị
```

Các option icon có sẵn:
- **Option 1**: Icon chữ V (mặc định) ✅
- **Option 2**: Hình vuông đơn giản
- **Option 3**: Hình tròn đơn giản  
- **Option 4**: Icon spike bomb

### Bước 2: Tạo icon
```powershell
python app_icon.py
```

File `icon.png` sẽ được tạo trong thư mục D:\Spike\

### Bước 3: Áp dụng vào app

#### Cách 1: Sử dụng icon.png có sẵn
Mở `timer_valo.py`, tìm hàm `create_tray_icon()` (khoảng dòng 275):

Thay đổi từ:
```python
def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='#ff4655')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill='white')
```

Thành:
```python
def create_tray_icon():
    try:
        image = Image.open('icon.png')
    except:
        # Fallback nếu không tìm thấy file
        image = Image.new('RGB', (64, 64), color='#ff4655')
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill='white')
```

#### Cách 2: Sử dụng icon.png cho cả exe icon
Build lại với tham số `--icon`:
```powershell
python -m PyInstaller --onefile --windowed --name "ValTimer" --icon=icon.png timer_valo.py --noconfirm
```

**Lưu ý**: Icon phải là file `.ico` nếu dùng cho exe. Có thể convert:
```powershell
# Cài đặt pillow nếu chưa có
pip install pillow

# Convert icon.png thành icon.ico
python -c "from PIL import Image; img = Image.open('icon.png'); img.save('icon.ico', format='ICO', sizes=[(64,64)])"
```

## Các màu Valorant đề xuất

```python
BACKGROUND_COLOR = '#ff4655'  # Valorant Red (hiện tại)
BACKGROUND_COLOR = '#0f1923'  # Valorant Dark Blue
BACKGROUND_COLOR = '#ece8e1'  # Valorant Off-white
BACKGROUND_COLOR = '#fd4556'  # Bright Red
```

## Nếu muốn dùng icon tùy chỉnh hoàn toàn

1. Tạo file `icon.png` (64x64 pixels) bằng tool vẽ (Paint, Photoshop, GIMP, etc.)
2. Lưu vào `D:\Spike\icon.png`
3. Sửa code như Cách 1 ở trên
4. Build lại app

## Debug

Nếu icon không hiển thị:
- Kiểm tra file `icon.png` có tồn tại không
- Kiểm tra kích thước (nên là 64x64)
- Xem log lỗi trong terminal khi chạy app
- Đảm bảo file icon.png nằm cùng folder với ValTimer.exe

## Quick start

Để nhanh chóng thay icon đỏ V hiện tại:

```powershell
# 1. Tạo icon mặc định
python app_icon.py

# 2. Sửa timer_valo.py (thay image = Image.new(...) bằng image = Image.open('icon.png'))

# 3. Build lại
python -m PyInstaller --onefile --windowed --name "ValTimer" timer_valo.py --noconfirm
```

Xong! ✅

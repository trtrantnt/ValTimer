"""
Script to customize ValTimer system tray icon
Chỉnh sửa icon cho app ValTimer

Usage:
1. Thay đổi màu sắc hoặc hình dạng trong hàm create_icon() bên dưới
2. Chạy: python app_icon.py
3. Icon mới sẽ được tạo và lưu vào icon.png
4. Build lại app để áp dụng icon mới

"""
from PIL import Image, ImageDraw, ImageFont

def create_icon(size=64, bg_color='#ff4655', fg_color='white', text='V'):
    """
    Tạo icon cho app
    
    Parameters:
    - size: Kích thước icon (64x64 pixels)
    - bg_color: Màu nền (hex color, ví dụ: '#ff4655' cho màu đỏ Valorant)
    - fg_color: Màu chữ (hex color hoặc tên màu: 'white', 'black', etc.)
    - text: Ký tự hiển thị trên icon ('V' cho Valorant)
    
    Returns:
    - PIL Image object
    """
    # Tạo ảnh nền
    image = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # OPTION 1: Icon kiểu chữ V (mặc định)
    try:
        # Thử dùng font Segoe UI Bold
        font = ImageFont.truetype("segoeui.ttf", int(size * 0.6))
    except:
        # Fallback: dùng font mặc định
        font = ImageFont.load_default()
    
    # Vẽ chữ V ở giữa
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - 4)
    draw.text(position, text, fill=fg_color, font=font)
    
    # OPTION 2: Icon kiểu hình vuông (bỏ comment dòng dưới nếu muốn dùng)
    # draw.rectangle([size//4, size//4, 3*size//4, 3*size//4], fill=fg_color)
    
    # OPTION 3: Icon kiểu hình tròn (bỏ comment dòng dưới nếu muốn dùng)
    # draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], fill=fg_color)
    
    # OPTION 4: Icon spike bomb (bỏ comment dòng dưới nếu muốn dùng)
    # draw_spike_icon(draw, size, fg_color)
    
    return image


def draw_spike_icon(draw, size, color):
    """Vẽ icon spike đơn giản"""
    center_x = size // 2
    center_y = size // 2
    radius = size // 4
    
    # Vẽ hình bầu dục (spike body)
    draw.ellipse([center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius], fill=color)
    
    # Vẽ các cọc nhọn
    spike_points = [
        (center_x, center_y - radius - 8),  # Top
        (center_x + radius + 8, center_y),  # Right
        (center_x, center_y + radius + 8),  # Bottom
        (center_x - radius - 8, center_y),  # Left
    ]
    
    for px, py in spike_points:
        draw.line([(center_x, center_y), (px, py)], fill=color, width=3)


# ============================================
# TÙY CHỈNH ICON Ở ĐÂY
# ============================================

# Màu sắc
BACKGROUND_COLOR = '#ff4655'  # Đỏ Valorant
TEXT_COLOR = 'white'          # Trắng
ICON_TEXT = 'V'               # Chữ hiển thị

# Tạo icon
icon = create_icon(
    size=64, 
    bg_color=BACKGROUND_COLOR, 
    fg_color=TEXT_COLOR, 
    text=ICON_TEXT
)

# Lưu icon ra file
icon.save('D:\\Spike\\icon.png')
print("✅ Icon đã được tạo: D:\\Spike\\icon.png")
print("\nĐể áp dụng icon:")
print("1. Mở timer_valo.py")
print("2. Tìm dòng: image = Image.new('RGB', (64, 64), color='#ff4655')")
print("3. Thay bằng: image = Image.open('icon.png')")
print("4. Build lại: python -m PyInstaller --onefile --windowed --name \"ValTimer\" --icon=icon.png timer_valo.py --noconfirm")
print("\nHoặc chạy CUSTOM_ICON.md để xem hướng dẫn chi tiết")

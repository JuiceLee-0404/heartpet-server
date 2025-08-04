# generate_placeholders.py
import os
from PIL import Image, ImageDraw, ImageFont

# -------- 可自定义区域 --------
PET1_COLOR = (181, 134,  91)   # pet1 主体色（棕）
PET2_COLOR = ( 60,  60,  60)   # pet2 主体色（灰）
BG_COLOR   = None              # 透明背景
IMAGE_SIZE = (80, 80)
# -------------------------------

# 生成纯色 8x8 像素块，再放大到 80x80
def make_pixel_icon(color, text=""):
    base = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rectangle([2, 2, 5, 5], fill=color)              # 小狗身体
    d.rectangle([3, 1, 4, 1], fill=color)                # 耳朵
    d.point([3, 6], fill=(0, 0, 0, 255))                # 左眼
    d.point([4, 6], fill=(0, 0, 0, 255))                # 右眼
    img = base.resize(IMAGE_SIZE, Image.NEAREST)
    if text:
        draw = ImageDraw.Draw(img)
        try:
            fnt = ImageFont.truetype("arial.ttf", 10)
        except OSError:
            fnt = ImageFont.load_default()
        draw.text((2, 2), text, fill=(255, 255, 255, 255), font=fnt)
    return img

# 目录结构
structure = {
    "pet1": ["idle", "happy", "sad", "angry", "proud", "shy", "surprised", "interactions"],
    "pet2": ["idle", "happy", "sad", "angry", "proud", "shy", "surprised", "interactions"]
}

# 生成函数
def generate(pet_name, color):
    for folder in structure[pet_name]:
        for i in range(1, 5):
            if folder == "interactions":
                fname = f"{folder}/{pet_name}/interactions/pat_{i:02d}.png"
            else:
                fname = f"{folder}/{pet_name}/{folder}/{folder}_{i:02d}.png"
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            img = make_pixel_icon(color, text=str(i))
            img.save(fname)

# 生成两组资源
generate("pet1", PET1_COLOR)
generate("pet2", PET2_COLOR)

print("✅ 所有占位符图片已生成完毕！")
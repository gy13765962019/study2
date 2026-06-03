"""
更新 hotspot 图标 —— 用户要求：
1) 干净的向前箭头（指向上=旋转后指向前方），背景纯透明
2) 不带任何圆环/底盘/中心点等"非箭头"元素
3) 配合自定义 GLSL shader 实现箭头内部的"流光"效果

设计：256x256 RGBA PNG
- 极淡的外发光（alpha < 45，柔和过渡）
- 白色描边的青色大箭头
- 内部一条亮色高光条（模拟流光在箭头内的通道）
"""
from PIL import Image, ImageDraw
import os

OUT_DIR = r"D:\2026_2_work\lihui\work3\assets\hotspot"
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 256
CX = SIZE // 2


def make_forward():
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, 'RGBA')

    # 极淡的柔光晕（无硬边）
    for r in range(95, 0, -2):
        alpha = int(45 * (1 - r / 95) ** 2)
        if alpha < 1:
            continue
        d.ellipse([CX - r, 128 - r, CX + r, 128 + r],
                  fill=(0, 212, 255, alpha))

    # ---- 箭头几何参数 ----
    tip_y  = 24
    wing_y = 96
    base_y = 232

    # 白色描边（外缘大 6px）
    outline = [
        (CX, tip_y - 6),
        (CX + 60, wing_y + 18),
        (CX + 26, wing_y + 18),
        (CX + 26, base_y + 6),
        (CX - 26, base_y + 6),
        (CX - 26, wing_y + 18),
        (CX - 60, wing_y + 18),
    ]
    d.polygon(outline, fill=(255, 255, 255, 235))

    # 青色主体填充
    fill = [
        (CX, tip_y),
        (CX + 50, wing_y + 12),
        (CX + 20, wing_y + 12),
        (CX + 20, base_y),
        (CX - 20, base_y),
        (CX - 20, wing_y + 12),
        (CX - 50, wing_y + 12),
    ]
    d.polygon(fill, fill=(0, 212, 255, 255))

    # 内部亮色高光条（让流光 shader 沿此条扫过更明显）
    inner = [
        (CX, tip_y + 18),
        (CX + 26, wing_y + 18),
        (CX + 8,  wing_y + 18),
        (CX + 8,  base_y - 8),
        (CX - 8,  base_y - 8),
        (CX - 8,  wing_y + 18),
        (CX - 26, wing_y + 18),
    ]
    d.polygon(inner, fill=(190, 245, 255, 220))

    out_path = os.path.join(OUT_DIR, 'forward.png')
    img.save(out_path, 'PNG', optimize=True)
    print('forward.png:', os.path.getsize(out_path), 'bytes')


if __name__ == '__main__':
    make_forward()

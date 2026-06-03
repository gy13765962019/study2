"""
重新生成 hotspot 图标 —— 用户要求：
1) 主体是指向前进（向上）的清晰箭头，不能是被淹没的图标
2) 整体必须动态（呼吸 + 扩散环 + 轻微旋转）
3) 背景必须透明，不能是色块遮挡全景

设计：256x256 透明 PNG
- 大三角箭头（cyan #00d4ff）做主体
- 一圈细描边白圈包住箭头
- 底下一个浅色光晕（半透明，中心稍亮）
"""
from PIL import Image, ImageDraw
import math
import os

OUT_DIR = r"D:\2026_2_work\lihui\work3\assets\hotspot"
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 256
CENTER = SIZE // 2

# ============================================================
# 1) 主热点图：透明背景 + 向上大箭头 + 白色描边圈 + 中心小圆点
# ============================================================
def make_forward():
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, 'RGBA')

    # 外层柔光圈（很淡的青色外发光，靠边缘处）
    for r in range(110, 0, -1):
        alpha = int(60 * (1 - r/110) ** 2)
        if alpha < 1:
            continue
        d.ellipse([CENTER-r, CENTER-r, CENTER+r, CENTER+r],
                  fill=(0, 212, 255, alpha))

    # 圆形底盘（深色透明，contrast 用）
    d.ellipse([CENTER-78, CENTER-78, CENTER+78, CENTER+78],
              fill=(8, 20, 40, 200), outline=(0, 212, 255, 255), width=3)

    # 中心白点
    d.ellipse([CENTER-8, CENTER-8, CENTER+8, CENTER+8],
              fill=(255, 255, 255, 255))

    # 向上大箭头（cyan + 白边）
    # 箭头由两个三角形组成：箭头顶 + 箭头底座
    arrow_color = (0, 212, 255, 255)
    arrow_edge  = (255, 255, 255, 230)

    # 箭头顶部三角（指向上方）
    tip = (CENTER, CENTER - 58)            # 箭头顶点
    base_l = (CENTER - 26, CENTER - 18)
    base_r = (CENTER + 26, CENTER - 18)
    # 箭头底部矩形
    body_l_top = (CENTER - 14, CENTER - 18)
    body_r_top = (CENTER + 14, CENTER - 18)
    body_l_bot = (CENTER - 14, CENTER + 38)
    body_r_bot = (CENTER + 14, CENTER + 38)

    # 整体外缘（白色描边）—— 把三角形和矩形合并成一个多边形
    outline_pts = [
        tip,
        (CENTER - 30, CENTER - 14),
        (CENTER - 14, CENTER - 14),
        (CENTER - 14, CENTER + 42),
        (CENTER + 14, CENTER + 42),
        (CENTER + 14, CENTER - 14),
        (CENTER + 30, CENTER - 14),
    ]
    # 先画白色描边（稍大）
    d.polygon(outline_pts, fill=arrow_edge)
    # 内部缩小版（青色）
    inner_pts = [
        (CENTER, CENTER - 50),
        (CENTER - 22, CENTER - 12),
        (CENTER - 8,  CENTER - 12),
        (CENTER - 8,  CENTER + 36),
        (CENTER + 8,  CENTER + 36),
        (CENTER + 8,  CENTER - 12),
        (CENTER + 22, CENTER - 12),
    ]
    d.polygon(inner_pts, fill=arrow_color)

    img.save(os.path.join(OUT_DIR, 'forward.png'), 'PNG', optimize=True)
    print('forward.png  size:', os.path.getsize(os.path.join(OUT_DIR, 'forward.png')))


# ============================================================
# 2) 扩散环 1：细青色描边圆环
# ============================================================
def make_ring(name, radius, width, color):
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, 'RGBA')
    d.ellipse([CENTER-radius, CENTER-radius, CENTER+radius, CENTER+radius],
              outline=color, width=width)
    img.save(os.path.join(OUT_DIR, name), 'PNG', optimize=True)
    print(name, ' size:', os.path.getsize(os.path.join(OUT_DIR, name)))


make_forward()
make_ring('ring.png',  radius=70, width=4, color=(0, 212, 255, 255))
make_ring('ring2.png', radius=50, width=3, color=(124, 255, 212, 255))

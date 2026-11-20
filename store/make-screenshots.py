# App Store用の見出しつきスクリーンショットを作る（raw → screenshots）。見本データ（作り話の数字）で撮影。
import os
from PIL import Image, ImageDraw, ImageFont
O = os.path.dirname(os.path.abspath(__file__))
W, H = 1320, 2868
fs = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", 52)
# (ファイル, 見出し, 小見出し, 上から切り取るpx)
shots = [
    ("02-counts",   "毎日の宅配記録を、もっと簡単に。", "件数を入れるだけで、売上を自動計算", 0),
    ("01-top",      "売上・勤務・走行を、まとめて管理。", "出庫・入庫やメンテナンス時期もひと目で", 0),
    ("03-calendar", "売上や休日を、カレンダーで確認。", "祝日・楽天セールも表示。PDFで印刷できる", 0),
    ("04-summary-clean", "月間・年間の売上を、自動で集計。", "1日平均の件数・売上もわかる", 0),
    ("05-settings", "項目も単価も、自分の仕事に合わせて。", "変えても、過去の売上はそのまま", 0),
]
BG, PANEL, TITLE, SUB = (226, 236, 252), (196, 214, 244), (21, 88, 200), (70, 86, 110)
out = f"{O}/screenshots"; os.makedirs(out, exist_ok=True)
for n, (f, t, s, crop) in enumerate(shots, 1):
    bg = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(bg)
    size = 100
    while True:
        fb = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc", size)
        if d.textlength(t, font=fb) < W - 110: break
        size -= 4
    for txt, font, y, col in ((t, fb, 170, TITLE), (s, fs, 330, SUB)):
        w = d.textlength(txt, font=font); d.text(((W - w) / 2, y), txt, font=font, fill=col)
    im = Image.open(f"{O}/raw/{f}.png").convert("RGB")
    if crop: im = im.crop((0, crop, im.width, im.height))
    sw = 1100; sh = int(im.height * sw / im.width); im = im.resize((sw, sh), Image.LANCZOS)
    m = Image.new("L", (sw, sh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sw, sh + 200), radius=90, fill=255)
    x = (W - sw) // 2; y = 470
    d.rounded_rectangle((x - 6, y - 6, x + sw + 6, y + sh + 300), radius=96, fill=PANEL)
    bg.paste(im, (x, y), m)
    bg.save(f"{out}/{n:02d}.png")
print("ok")

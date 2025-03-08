# 指定した部分を白にしたマスク画像を作成 

from PIL import Image
import numpy as np

# 元の画像と同じサイズのマスクを作成
image = Image.open("input.png").convert("RGB")
mask = np.zeros((image.height, image.width), dtype=np.uint8)

# 例: 画像の中央部分だけを変更したい場合
h, w = mask.shape
mask[h//4: 3*h//4, w//4: 3*w//4] = 255  # 中央を白くする

# マスク画像を保存
mask_image = Image.fromarray(mask)
mask_image.save("mask.png")
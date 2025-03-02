import cv2
import torch

# YOLOv5のモデルをロード
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# カメラ映像をキャプチャ
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # AI解析
    results = model(frame)

    # 検出結果をフレームに描画
    for img in results.render():  # YOLOv5の結果を取得
        frame = img  # 画像を更新

    # 結果を表示
    cv2.imshow('Security Cam', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

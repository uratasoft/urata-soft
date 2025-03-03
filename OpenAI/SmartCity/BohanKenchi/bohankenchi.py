# スマート防犯システム（AI異常検知）
# YOLO（You Only Look Once）とは物体検出のための深層学習アルゴリズム

import cv2  # OpenCV（カメラ映像取得）
import torch  # PyTorch（YOLOを動かすため）
import datetime  # 日時の取得
import winsound  # 音声アラート（Windows）
#import smtplib  # メール送信
#from email.mime.text import MIMEText  # メール送信用
from ultralytics import YOLO  # 最新の YOLOv8 を使用

# 🔹 GPUを使用可能ならCUDA、なければCPUを使用
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 🔹 YOLOv8モデルをロード（物体検出用）
model = YOLO("yolov8s.pt")

# 🔹 カメラを開く（0はデフォルトのカメラ）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラが開けませんでした。プログラムを終了します。")
    exit()

# 🔹 監視ログファイルを作成
log_file = "detection_log.txt"

with open(log_file, "w") as f:
    f.write("=== 監視カメラログ ===\n")

# 🔹 メール通知設定
EMAIL_SENDER = "my@address"
EMAIL_PASSWORD = "passwd"
EMAIL_RECEIVER = "my@address"

def send_alert(message):
    """ 検出した異常をメールで送信 """
    msg = MIMEText(message)
    msg["Subject"] = "【監視カメラアラート】異常検出"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("📩 メール通知を送信しました！")
    except Exception as e:
        print("⚠️ メール通知の送信に失敗しました:", e)
        
# 🔹 監視を続ける
while True:
    ret, frame = cap.read()  # カメラの映像を取得
    if not ret:
        print("カメラの映像が取得できません。終了します。")
        break

    # 🔹 YOLOv8 で物体検出
    results = model(frame)

    # 🔹 検出されたオブジェクトをログに記録
    detected_objects = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # クラスID（例：人、車、犬など）
            confidence = float(box.conf[0])  # 信頼度
            label = model.names[class_id]  # クラス名（YOLOのラベル）

            # ログに保存
            detected_objects.append(f"{label}（信頼度: {confidence:.2f}）")

    # 🔹 もし物体が検出されたらログに書き込み、アラートを鳴らす
    if detected_objects:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"{now} - 検出: {', '.join(detected_objects)}\n"
        print(log_text)

        with open(log_file, "a") as f:
            f.write(log_text)

        # 🔹 スクリーンショットを保存
        filename = f"screenshot_{now.replace(':', '-')}.jpg"
        cv2.imwrite(filename, frame)

        # 🔹 音声アラート（Windowsのみ）
        winsound.Beep(1000, 500)  # 1kHzの音を0.5秒鳴らす

        # 🔹 メール通知
        #send_alert(log_text)

    # 🔹 YOLOの検出結果を描画
    frame_with_detections = results[0].plot()

    # 🔹 画面にリアルタイム映像を表示
    cv2.imshow("Security Cam", frame_with_detections)

    # 🔹 'q'キーで監視終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🔹 カメラを解放し、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()

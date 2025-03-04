"""
市民の健康チェック（OpenAI APIを利用）
地元医療機関への連携（仮想データベース & 通知）
服薬リマインド（スケジューリング機能）
訪問看護師の手配（自動リクエスト機能）
家族への通知（メール通知機能）
GPT-4oで健康診断を分析し、緊急度を評価
✔ 診断結果に応じて、医療機関や訪問看護師へ自動通知
✔ 家族へメールで健康状況を通知
✔ 毎日指定時間に服薬リマインドを実行（スケジューリング機能）
"""
import os
import time
import json
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
from datetime import datetime, timedelta
import schedule #標準ライブラリには存在しない

# OpenAI API クライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ユーザーの健康データ（仮データ）
citizen_health_data = {
    "user_id": "12345",
    "name": "田中 一郎",
    "age": 72,
    "symptoms": ["微熱 (37.8℃)", "血圧が高め (145/90)", "咳が続く", "倦怠感"],
    "medications": ["降圧剤（1日1回 朝）", "咳止め（1日2回 朝・夜）"],
    "emergency_contact": "family@example.com",
    "location": "千葉県柏市",
}

# 医療機関データ（仮のデータベース）
local_medical_centers = {
    "柏市総合病院": {"address": "柏市〇〇1-2-3", "contact": "0471-XXX-XXX"},
    "柏中央クリニック": {"address": "柏市〇〇4-5-6", "contact": "0471-YYY-YYY"},
}

# 訪問看護師のリスト（仮データ）
visiting_nurses = [
    {"name": "佐藤 看護師", "contact": "0471-ABC-DEF"},
    {"name": "鈴木 看護師", "contact": "0471-GHI-JKL"},
]


# 🔹 市民の健康チェック (GPT-4oで分析)
def analyze_health_status():
    """GPT-4o を使って健康状態を解析し、医療機関連携や家族通知の必要性を判断"""
    prompt = f"""
    以下の健康データを基に、緊急性の有無と適切な対応を判断してください。
    
    【健康データ】
    - 名前: {citizen_health_data["name"]}
    - 年齢: {citizen_health_data["age"]}
    - 症状: {', '.join(citizen_health_data['symptoms'])}

    【診断結果フォーマット】
    - 緊急性: （低 / 中 / 高）
    - 推奨対応: （例: 近隣の医療機関を受診 / 訪問看護師の派遣 / 経過観察）
    - コメント: （追加アドバイス）
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    diagnosis = response.choices[0].message.content
    print("\n📋 **健康診断結果**")
    print(diagnosis)

    return diagnosis


# 🔹 地元医療機関への連携
def notify_medical_center(diagnosis):
    """診断結果が中〜高緊急度の場合、地元医療機関へ通知"""
    if "高" in diagnosis or "中" in diagnosis:
        selected_center = list(local_medical_centers.keys())[0]  # 仮に最寄りの病院を選択
        print(f"\n🏥 {selected_center} へ通知しました。")
        print(f"連絡先: {local_medical_centers[selected_center]['contact']}")


# 🔹 訪問看護師の手配
def dispatch_nurse(diagnosis):
    """緊急性が高い場合、訪問看護師を手配"""
    if "高" in diagnosis:
        nurse = visiting_nurses[0]  # 仮に最初の看護師を選択
        print(f"\n🚑 訪問看護師 {nurse['name']} を手配しました。")
        print(f"連絡先: {nurse['contact']}")


# 🔹 家族へ通知（メール送信）
def notify_family(diagnosis):
    """緊急性が中〜高のときに家族へメール通知"""
    if "高" in diagnosis or "中" in diagnosis:
        recipient = citizen_health_data["emergency_contact"]
        subject = f"【健康通知】{citizen_health_data['name']} さんの健康状態について"
        body = f"健康診断結果:\n\n{diagnosis}\n\n適切な対応をお願いします。"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "healthcare@smartcity.com"
        msg["To"] = recipient

        try:
            with smtplib.SMTP("smtp.example.com") as server:
                server.sendmail("healthcare@smartcity.com", recipient, msg.as_string())
            print(f"\n📩 家族へ通知を送信しました。（宛先: {recipient}）")
        except Exception as e:
            print(f"\n⚠️ メール送信失敗: {e}")


# 🔹 服薬リマインド（スケジューリング）
def remind_medications():
    """毎日指定の時間に服薬をリマインド"""
    now = datetime.now().strftime("%H:%M")
    for med in citizen_health_data["medications"]:
        print(f"🕒 {now} - 服薬リマインド: {med}")


# 🔹 スケジューリング（定期実行）
schedule.every().day.at("08:00").do(remind_medications)  # 朝の服薬リマインド
schedule.every().day.at("20:00").do(remind_medications)  # 夜の服薬リマインド


# 🔹 メイン実行
if __name__ == "__main__":
    diagnosis_result = analyze_health_status()
    notify_medical_center(diagnosis_result)
    dispatch_nurse(diagnosis_result)
    notify_family(diagnosis_result)

    while True:
        schedule.run_pending()  # 服薬リマインドのスケジューリングを実行
        time.sleep(60)

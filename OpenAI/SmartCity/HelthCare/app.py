import os
import json
import time
import schedule
import smtplib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from openai import OpenAI

# Flask アプリの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# OpenAI API 初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# **データベースモデル**
class CitizenHealth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    symptoms = db.Column(db.String(255), nullable=False)
    medications = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=False)

class Nurse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)

# DB 初期化
with app.app_context():
    db.create_all()

# **健康データ登録**
@app.route('/health', methods=['GET', 'POST'])
def register_health():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        symptoms = request.form['symptoms']
        medications = request.form['medications']
        emergency_contact = request.form['emergency_contact']

        new_health = CitizenHealth(name=name, age=age, symptoms=symptoms,
                                   medications=medications, emergency_contact=emergency_contact)
        db.session.add(new_health)
        db.session.commit()

        # **GPT-4o による診断**
        diagnosis = analyze_health_status(name, age, symptoms)
        new_health.diagnosis = diagnosis
        db.session.commit()

        return redirect(url_for('health_list'))

    return render_template('register_health.html')

# **健康データ一覧**
@app.route('/health_records')
def health_list():
    health_records = CitizenHealth.query.all()
    return render_template('health_records.html', health_records=health_records)

# **GPT-4o による健康チェック**
def analyze_health_status(name, age, symptoms):
    prompt = f"""
    {name} さん（{age}歳）の健康状態を評価してください。
    【症状】{symptoms}
    診断結果：
    - 緊急性: (低 / 中 / 高)
    - 推奨対応: (例: 医療機関を受診 / 訪問看護師の派遣 / 経過観察)
    - コメント: (追加のアドバイス)
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content

# **家族へ通知**
def notify_family(health_data):
    recipient = health_data.emergency_contact
    subject = f"【健康通知】{health_data.name} さんの健康状態について"
    body = f"{health_data.diagnosis}\n\n適切な対応をお願いします。"

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

# **服薬リマインド**
def remind_medications():
    now = datetime.now().strftime("%H:%M")
    health_records = CitizenHealth.query.all()
    for record in health_records:
        print(f"🕒 {now} - {record.name} の服薬リマインド: {record.medications}")

# **スケジュール管理**
schedule.every().day.at("08:00").do(remind_medications)
schedule.every().day.at("20:00").do(remind_medications)

# Flask アプリ起動
if __name__ == '__main__':
    app.run(debug=True)

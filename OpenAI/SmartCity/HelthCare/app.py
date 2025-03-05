import os
import json
import logging
import smtplib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from openai import OpenAI

# Flaskアプリ設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# OpenAI API 初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ログ設定
logging.basicConfig(filename='healthcare.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# **データベースモデル**
class CitizenHealth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    symptoms = db.Column(db.String(255), nullable=False)
    medications = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=True, default="未診断")

class Nurse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)

class MedicalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(50), nullable=False)

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
        new_health.status = "診断済み"
        db.session.commit()

        log_action(f"✅ {name} さんの診断結果: {diagnosis}")

        # **緊急度が高い場合、医療機関と看護師を手配**
        if "高" in diagnosis:
            notify_medical_center(new_health)
            dispatch_nurse(new_health)
            notify_family(new_health)
            new_health.status = "緊急対応"
            db.session.commit()
        elif "中" in diagnosis:
            notify_family(new_health)
            new_health.status = "要注意"
            db.session.commit()
        else:
            new_health.status = "軽度"
            db.session.commit()

        return redirect(url_for('health_list'))

    return render_template('register_health.html')

# **健康データ一覧**
@app.route('/health_records')
def health_list():
    health_records = CitizenHealth.query.all()
    return render_template('health_records.html', health_records=health_records)

# **リアルタイム診断ログを表示**
@app.route('/logs')
def view_logs():
    with open('healthcare.log', 'r') as file:
        logs = file.readlines()
    return render_template('logs.html', logs=logs)

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

# **医療機関へ通知**
def notify_medical_center(health_data):
    medical_centers = MedicalCenter.query.all()
    if not medical_centers:
        return

    selected_center = medical_centers[0]
    log_action(f"🏥 {health_data.name} さんを {selected_center.name} に連絡")

# **訪問看護師を手配**
def dispatch_nurse(health_data):
    nurses = Nurse.query.all()
    if not nurses:
        return

    nurse = nurses[0]
    log_action(f"🚑 {health_data.name} さんに {nurse.name} 看護師を派遣")

# **家族へ通知**
def notify_family(health_data):
    log_action(f"📩 家族へ通知を送信: {health_data.name} さんの健康状態")

# **アクションログを記録**
def log_action(message):
    logging.info(message)

# **Flaskアプリ起動**
if __name__ == '__main__':
    app.run(debug=True)

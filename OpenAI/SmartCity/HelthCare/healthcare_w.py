# pip install flask flask-sqlalchemy flask-wtf wtforms
import os
import json
import smtplib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
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

class MedicalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(50), nullable=False)

# DB 初期化
with app.app_context():
    db.create_all()

# **看護師の登録ページ**
@app.route('/nurse', methods=['GET', 'POST'])
def register_nurse():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        specialty = request.form['specialty']

        new_nurse = Nurse(name=name, contact=contact, specialty=specialty)
        db.session.add(new_nurse)
        db.session.commit()
        return redirect(url_for('nurse_list'))

    return render_template('register_nurse.html')

# **看護師リストの表示**
@app.route('/nurses')
def nurse_list():
    nurses = Nurse.query.all()
    return render_template('nurses.html', nurses=nurses)

# **医療機関の登録ページ**
@app.route('/medical_center', methods=['GET', 'POST'])
def register_medical_center():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        contact = request.form['contact']

        new_center = MedicalCenter(name=name, location=location, contact=contact)
        db.session.add(new_center)
        db.session.commit()
        return redirect(url_for('medical_center_list'))

    return render_template('register_medical_center.html')

# **医療機関リストの表示**
@app.route('/medical_centers')
def medical_center_list():
    centers = MedicalCenter.query.all()
    return render_template('medical_centers.html', centers=centers)

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

        # **登録された医療機関・看護師を利用**
        notify_medical_center(new_health)
        dispatch_nurse(new_health)
        notify_family(new_health)

        return redirect(url_for('health_list'))

    return render_template('register_health.html')

# **医療機関へ通知**
def notify_medical_center(health_data):
    medical_centers = MedicalCenter.query.all()
    if not medical_centers:
        return

    selected_center = medical_centers[0]  # 最初の登録病院を仮選択
    print(f"\n🏥 {selected_center.name} へ通知しました。（{selected_center.contact}）")

# **訪問看護師を手配**
def dispatch_nurse(health_data):
    nurses = Nurse.query.all()
    if not nurses:
        return

    nurse = nurses[0]  # 最初の登録看護師を仮選択
    print(f"\n🚑 {nurse.name} 看護師を派遣しました。（{nurse.contact}）")

# **Flaskアプリ起動**
if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return redirect(url_for('main.login'))


@main.route('/admin/dashboard')
def dashboard_admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Silakan login sebagai admin.', 'error')
        return redirect(url_for('main.login'))
    return render_template('dashboard_admin.html')



@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, role FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            if user[2] != 'admin':
                flash('Hanya admin yang dapat login saat ini.', 'error')
                return render_template('login_register.html')

            # Simpan session dan redirect ke dashboard admin
            session['user_id'] = user[0]
            session['role'] = user[2]
            flash('Login admin berhasil.', 'success')
            return redirect(url_for('main.dashboard_admin'))
        else:
            flash('Email atau password salah.', 'error')
            return render_template('login_register.html')

    return render_template('login_register.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            flash('Email sudah digunakan.', 'error')
            cur.close()
            return render_template('login_register.html')

        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_pw, 'pengguna'))
        mysql.connection.commit()
        cur.close()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('login_register.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('main.login'))


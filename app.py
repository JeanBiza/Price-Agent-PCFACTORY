from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, get_active_products, add_product, delete_product, get_history, add_user, \
    get_id_from_email, check_password, get_user, update_user, product_exists, check_mail_exist
from scraper import get_product_from_url
from tools import sent_random_code
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if check_mail_exist(email):
            return render_template('register.html', error="Este correo ya existe")

        if password != confirm_password:
            return render_template('register.html', error="Las contraseñas no coinciden")

        code = sent_random_code(email)
        session['register_code'] = code
        session['register_email'] = email
        session['register_password'] = password
        return redirect(url_for('verify'))

    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_code = request.form.get('user_code')
        if int(user_code) == session.get('register_code'):
            add_user(session['register_email'], session['register_password'], None)
            session.clear()
            return redirect(url_for('login'))
        else:
            return render_template('verify.html', error="Código incorrecto")

    return render_template('verify.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not check_password(email, password):
            return render_template('login.html', error="Credenciales incorrectas")
        session["user_id"] = get_id_from_email(email)
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    url = request.form.get('url')
    threshold = request.form.get('threshold')

    if not url or not threshold:
        return render_template('index.html', error="Campos requeridos")

    try:
        threshold = float(threshold)
    except ValueError:
        return render_template('index.html', error="Umbral inválido")

    result = get_product_from_url(url)
    if result is None:
        return redirect(url_for('index'))

    name, price, image = result
    if not product_exists(url, user_id):
        add_product(url, name, float(threshold), user_id)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    product_id = request.form.get('id')
    delete_product(int(product_id))
    return redirect(url_for('index'))

@app.route('/history/<int:product_id>')
def history_prices(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    products = get_active_products(user_id)
    product = next((p for p in products if p[0] == product_id), None)
    if product is None:
        return redirect(url_for('index'))
    history = get_history(product[1], user_id)
    return render_template('history.html', product=product, history=history)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = get_user(user_id)
    if request.method == "POST":
        email = request.form.get('email')
        telegram_id = request.form.get('telegram_id')
        update_user(user_id, email, telegram_id)
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    products = get_active_products(user_id) or []
    return render_template('index.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
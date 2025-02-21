from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import requests
from datetime import datetime as dt
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

class InfoForm(FlaskForm):
    valor_produto = StringField('Valor do produto', validators=[DataRequired()])
    parcela = StringField('Número de parcelas', validators=[DataRequired()])
    taxa = StringField('Taxa de juros de seu rendimento mensal (%)', validators=[DataRequired()])
    contato = TextAreaField('Entre em contato', render_kw={"rows": 3, "cols": 40})
    submit = SubmitField('Calcular')
    reset = SubmitField('Limpar')

class Gibeira:
    def __init__(self, valor_produto, parcela, taxa):
        self.valor_produto = float(valor_produto)
        self.parcela = int(parcela)
        self.taxa = float(taxa)
        self.calculo = 0

    def calc(self):
        v_parcelas = self.valor_produto / self.parcela
        for i in range(self.parcela):
            self.calculo += (self.valor_produto - i * v_parcelas + self.calculo) * self.taxa
        return round(self.calculo, 2)

# obter o IP do cliente
def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

# localização a partir do IP
def get_location(ip):
    url = f'http://ipinfo.io/{ip}/json'
    data = requests.get(url).json()
    return data.get('loc', '0,0')

# carregar o .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# mongodb
client = MongoClient(MONGO_URI)
db = client['db_gibeira']
logs_collection = db['logs']

# save
def save_log_to_db(ip, message):
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    location = get_location(ip)

    log_data = {
        "ip": ip,
        "location": location,
        "message": message,
        "timestamp": timestamp
    }

    logs_collection.insert_one(log_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    calculo = None  
    message_status = None

    ip = get_client_ip()
    location = get_location(ip)
    google_maps_url = f'https://www.google.com/maps?q={location}'

    # save sem msg
    if request.method == 'GET':
        save_log_to_db(ip, "Acesso ao site")  

    if form.validate_on_submit():
        if form.submit.data:
            try:
                valor_produto = form.valor_produto.data
                parcela = form.parcela.data
                taxa = form.taxa.data.replace(',', '.')

                gib = Gibeira(valor_produto, parcela, taxa)
                calculo = gib.calc()
            except ValueError:
                calculo = "Erro nos dados inseridos"

        elif form.reset.data:
            return redirect(url_for('index'))
    
    # msg
    if request.method == 'POST':
        mensagem = request.form.get('mensagem', '').strip()
        if mensagem:
            save_log_to_db(ip, mensagem)  # save no mongodb

    return render_template('1_gibeira.html', form=form, calculo=calculo, ip=ip, google_maps_url=google_maps_url, message_status=message_status)


if __name__ == '__main__':
    app.run(debug=True)

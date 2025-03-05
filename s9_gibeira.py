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


# CÁLCULO CRÉDITO INDEX
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
        self.taxa = float(taxa)/100
        self.calculo = 0
    def calc(self):
        v_parcelas = self.valor_produto / self.parcela
        for i in range(self.parcela):
            self.calculo += (self.valor_produto - i * v_parcelas + self.calculo) * self.taxa
        return round(self.calculo, 2)


# função para obter o IP do cliente
def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

# função para obter a localização a partir do IP
def get_location(ip):
    url = f'http://ipinfo.io/{ip}/json'
    data = requests.get(url).json()
    return data.get('loc', '0,0')

# carregar variáveis do .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# conectar ao mongodb
client = MongoClient(MONGO_URI)
db = client['db_gibeira']
logs_collection = db['logs']

# função para salvar logs no mongodb
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

# rota para index
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    calculo = None  
    message_status = None

    ip = get_client_ip()
    location = get_location(ip)
    google_maps_url = f'https://www.google.com/maps?q={location}'

    # salvar log mesmo sem mensagem
    if request.method == 'GET':
        save_log_to_db(ip, "Acesso ao site")  

    if form.validate_on_submit():
        if form.submit.data:  # botão de calcular
            try:
                valor_produto = form.valor_produto.data
                parcela = form.parcela.data
                taxa = form.taxa.data.replace(',', '.')

                gib = Gibeira(valor_produto, parcela, taxa)
                calculo = gib.calc()
            except ValueError:
                calculo = "Erro nos dados inseridos"

        elif form.reset.data:  # botão de limpar
            return redirect(url_for('index'))
    
    # Capturar a mensagem do formulário
    if request.method == 'POST':
        mensagem = request.form.get('mensagem', '').strip()
        if mensagem:
            save_log_to_db(ip, mensagem)  # salvar no mongodb

    return render_template('1_gibeira.html', form=form, calculo=calculo, ip=ip, google_maps_url=google_maps_url, message_status=message_status)


# rota para a página "TEMPO"
@app.route('/tempo', methods=['GET', 'POST'])
def tempo():
    from banco_tempo import TempoForm, calc_tempo  # importando função tempo

    form = TempoForm()
    resultado = None

    if form.validate_on_submit():
        resultado = calc_tempo(form.cf.data, form.cm.data, form.i.data, form.total.data)

    return render_template('tempo.html', form=form, resultado=resultado)

# rota para a página "TOTAL"
@app.route('/total', methods=['GET', 'POST'])
def total():
    from banco_total import TotalForm, calc_total

    form = TotalForm()
    resultado = None

    if form.validate_on_submit():
        resultado = calc_total(form.cf.data, form.cm.data, form.i.data, form.t.data)

    return render_template('total.html', form=form, resultado=resultado)

# rota para "SAC"
@app.route("/sac", methods=["GET", "POST"])
def sac():
    from banco_sac import SACForm, calcular_sac
    form = SACForm()
    parcelas = None
    total_juros = None

    if form.validate_on_submit():
        parcelas, total_juros = calcular_sac(form.sd.data, form.i.data, form.t.data)

    return render_template("sac.html", form=form, parcelas=parcelas, total_juros=total_juros)

# rota para "PRICE"
@app.route("/price", methods=["GET", "POST"])
def price():
    from banco_price import PriceForm, calcular_price
    form = PriceForm()
    parcelas = None
    total_juros = None

    if form.validate_on_submit():
        parcelas, total_juros = calcular_price(form.sd.data, form.i.data, form.t.data)

    return render_template("price.html", form=form, parcelas=parcelas, total_juros=total_juros)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import requests
from datetime import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

class InfoForm(FlaskForm):
    valor_produto = StringField('Valor do produto', validators=[DataRequired()])
    parcela = StringField('Número de parcelas', validators=[DataRequired()])
    taxa = StringField('Taxa de juros (%)', validators=[DataRequired()])
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

# Captura o IP público do usuário
def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip
def get_location(ip):
    url = f'http://ipinfo.io/{ip}/json'
    data = requests.get(url).json()
    return data.get('loc', '0,0')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    calculo = None  
    message_status = None

    ip = get_client_ip()
    location = get_location(ip)  # Obtém o IP antes da gravação no arquivo
    google_maps_url = f'https://www.google.com/maps?q={location}'

    if form.validate_on_submit():
        if form.submit.data:  # Se o botão de calcular for clicado
            try:
                valor_produto = form.valor_produto.data
                parcela = form.parcela.data
                taxa = form.taxa.data.replace(',', '.')

                gib = Gibeira(valor_produto, parcela, taxa)
                calculo = gib.calc()
            except ValueError:
                calculo = "Erro nos dados inseridos"

        elif form.reset.data:  # Se o botão de limpar for clicado
            return redirect(url_for('index'))
    
    # Salvar o IP no log com data/hora
    today = dt.now()
    today_str = today.strftime("%Y-%m-%d | %H:%M:%S")
    with open('ips.txt', 'a', encoding='utf-8') as ips:
        ips.write(f'{ip} - {today_str}\n')


    # msg.txt
    if request.method == 'POST':
        mensagem = request.form.get('mensagem', '').strip()
        if mensagem:
            with open('msg.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(f'ip:{ip}\n Message: {mensagem}\n Hora: {today_str}\n\n')
        else:
            pass

    return render_template('1_gibeira.html', form=form, calculo=calculo, ip=ip, google_maps_url=google_maps_url, message_status=message_status)

# Rota para baixar msg.txt
@app.route('/download-msg')
def download_msg():
    return send_file('msg.txt', as_attachment=True)

# Rota para baixar ips.txt
@app.route('/download-ips')
def download_ips():
    return send_file('ips.txt', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

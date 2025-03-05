from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'

# Formulário para entrada de dados
class PriceForm(FlaskForm):
    sd = StringField("Montante (R$)", validators=[DataRequired()])
    i = StringField("Juros Mensal (%)", validators=[DataRequired()])
    t = StringField("Número de Parcelas", validators=[DataRequired()])
    submit = SubmitField("Calcular")

# Função para calcular o sistema Price
def calcular_price(sd, i, t):
    try:
        sd = float(sd.replace(",", "."))  # Convertendo para float
        i = float(i.replace(",", "."))/100
        t = int(t)  # Convertendo para inteiro

        # Cálculo da parcela fixa (PMT)
        pmt = (sd * i * (1 + i) ** t) / (((1 + i) ** t) - 1)

        saldo_devedor = sd
        total_juros = 0
        parcelas = []

        for mes in range(1, t + 1):
            juro = saldo_devedor * i  # Cálculo dos juros
            amortizacao = pmt - juro  # Amortização
            saldo_devedor -= amortizacao  # Atualizando saldo devedor
            total_juros += juro  # Acumulando juros pagos

            parcelas.append({
                "mes": mes,
                "parcela": round(pmt, 2),
                "juros": round(juro, 2),
                "amortizacao": round(amortizacao, 2),
                "saldo_devedor": max(round(saldo_devedor, 2), 0)  # Evita valores negativos
            })

        return parcelas, round(total_juros, 2)

    except ValueError:
        return None, None

# Rota para "Sistema Price"
# @app.route("/price", methods=["GET", "POST"])
# def price():
#     form = PriceForm()
#     parcelas = None
#     total_juros = None

#     if form.validate_on_submit():
#         parcelas, total_juros = calcular_price(form.sd.data, form.i.data, form.t.data)

#     return render_template("price.html", form=form, parcelas=parcelas, total_juros=total_juros)

if __name__ == "__main__":
    app.run(debug=True)

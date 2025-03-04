from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'

# form
class SACForm(FlaskForm):
    sd = StringField("Montante (R$)", validators=[DataRequired()])
    i = StringField("Juros Mensal (%)", validators=[DataRequired()])
    t = StringField("Número de Parcelas", validators=[DataRequired()])
    submit = SubmitField("Calcular")

def calcular_sac(sd, i, t):
    try:
        sd = float(sd.replace(",", "."))
        i = float(i.replace(",", "."))
        t = int(t)

        amort = sd / t  # amortização constante
        saldo_devedor = sd
        total_juros = 0
        parcelas = []

        for mes in range(1, t + 1):
            juro = saldo_devedor * i
            parcela = amort + juro
            saldo_devedor -= amort
            total_juros += juro

            parcelas.append({
                "mes": mes,
                "parcela": round(parcela, 2),
                "juros": round(juro, 2),
                "amortizacao": round(amort, 2),
                "saldo_devedor": round(saldo_devedor, 2)
            })

        return parcelas, round(total_juros, 2)

    except ValueError:
        return None, None

# rota para "SAC"
# @app.route("/sac", methods=["GET", "POST"])
# def sac():
#     form = SACForm()
#     parcelas = None
#     total_juros = None

#     if form.validate_on_submit():
#         parcelas, total_juros = calcular_sac(form.sd.data, form.i.data, form.t.data)

#     return render_template("sac.html", form=form, parcelas=parcelas, total_juros=total_juros)

if __name__ == "__main__":
    app.run(debug=True)

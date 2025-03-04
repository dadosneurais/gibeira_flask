from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta' # necessário para flaskform

# form
class TempoForm(FlaskForm):
    cf = StringField("Capital Fixo Inicial", validators=[DataRequired()])
    cm = StringField("Capital Adicionado Mensalmente", validators=[DataRequired()])
    i = StringField("Taxa de Rendimento Mensal (%)", validators=[DataRequired()])
    total = StringField("Montante Desejado", validators=[DataRequired()])
    submit = SubmitField("Calcular")

# Função de cálculo do tempo
def calc_tempo(cf, cm, i, total):
    try:
        cf = float(cf.replace(",", "."))
        cm = float(cm.replace(",", "."))
        i = float(i.replace(",", "."))
        total = float(total.replace(",", "."))

        log1 = math.log(((cm / i) + total) / ((cm / i) + cf))
        log2 = math.log(1 + i)

        t = log1 / log2
        return round(t, 2)

    except (ValueError, ZeroDivisionError):
        return None


# @app.route("/tempo", methods=["GET", "POST"])
# def tempo():
#     form = TempoForm()
#     resultado = None

#     if form.validate_on_submit():
#         resultado = calc_tempo(form.cf.data, form.cm.data, form.i.data, form.total.data)

#     return render_template("tempo.html", form=form, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)

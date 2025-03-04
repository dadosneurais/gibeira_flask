from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'


class TotalForm(FlaskForm):
    cf = StringField("Capital Fixo Inicial", validators=[DataRequired()])
    cm = StringField("Capital Adicionado Mensalmente", validators=[DataRequired()])
    i = StringField("Taxa de Rendimento Mensal (%)", validators=[DataRequired()])
    t = StringField("Tempo Desejado (meses)", validators=[DataRequired()])
    submit = SubmitField("Calcular")

# função de cálculo do montante total
def calc_total(cf, cm, i, t):
    try:
        cf = float(cf.replace(",", "."))
        cm = float(cm.replace(",", "."))
        i = float(i.replace(",", "."))
        t = int(t.replace(",", "."))

        if i == 0:
            soma = cf + (cm * t)  # se a taxa for zero
        else:
            soma = cf * (1 + i) ** t + cm * (((1 + i) ** t - 1) / i)

        return round(soma, 2)

    except (ValueError, ZeroDivisionError):
        return None


# @app.route("/total", methods=["GET", "POST"])
# def total():
#     form = TotalForm()
#     resultado = None

#     if form.validate_on_submit():
#         resultado = calc_total(form.cf.data, form.cm.data, form.i.data, form.t.data)

#     return render_template("total.html", form=form, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)

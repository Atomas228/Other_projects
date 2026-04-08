from flask_wtf import FlaskForm
from flask import Flask, render_template
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "secret"
class TextForm(FlaskForm):
    text = StringField("Text", validators=[DataRequired()])

morse_code = {
    'a': '.-',    'b': '-...',  'c': '-.-.',
    'd': '-..',   'e': '.',     'f': '..-.',
    'g': '--.',   'h': '....',  'i': '..',
    'j': '.---',  'k': '-.-',   'l': '.-..',
    'm': '--',    'n': '-.',    'o': '---',
    'p': '.--.',  'q': '--.-',  'r': '.-.',
    's': '...',   't': '-',     'u': '..-',
    'v': '...-',  'w': '.--',   'x': '-..-',
    'y': '-.--',  'z': '--..',
    ' ': '/'
}
@app.route('/', methods = ['GET', 'POST'])
def main():
    morse_txt = []
    form = TextForm()
    response = None
    if form.validate_on_submit():
        txt = form.text.data
        for i in txt.lower():
            if i in morse_code.keys():
                morse_txt.append(morse_code[i])
            else:
                morse_txt.append('(?)')
        response = ' '.join(morse_txt)
    return render_template("index.html", form=form, response=response)

if __name__ == "__main__":
    app.run(debug=True)
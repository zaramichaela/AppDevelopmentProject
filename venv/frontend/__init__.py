from flask import Flask, render_template
app = Flask(__name__)

@app.route('Home')
def Home(Homepage):
    return render_template("Home.html", name=Homepage)

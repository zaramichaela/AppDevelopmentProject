from backend import *
from flask import Flask

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

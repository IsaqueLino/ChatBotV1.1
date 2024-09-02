from flask import Flask, render_template, request, redirect, url_for, session
import os


app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = 'chatbot_v1.0'

@app.route('/')
def index():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
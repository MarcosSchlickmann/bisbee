from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/user/<nome>')
def user(nome):
	return render_template("user.html", name=nome)


@app.route('/navegador')
def navegador():
	user_agent = request.headers.get("User-Agent")
	return "<p>{}</p>".format(user_agent)


@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404
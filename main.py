"""
 APLICACION QUE SORTEA REGALOS DEL CORTE INGLES
 CON ADMIN DONDE INTRODUCIR LOS DATOS.
 CON ADMIN CON SCRAPPING AUTOMATIZADO

"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_bootstrap import Bootstrap
from ModuloMongo.MongoManger import managermongo
from TemplateFormularios.Admin import *

# inicializacion e instanciacion
app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/admin", methods=["GET"])
def home_admin():
    return render_template("admin_login.html")


@app.route("/admin_profile", methods=["GET"])
def admin_profile():
    return render_template("admin_profile.html")


@app.route("/admin_profile/alta", methods=["GET"])
def alta_producto():
    template_registrar_producto = FormularioRellanarProducto()

    return render_template("altaproducto.html", formulario=template_registrar_producto)

@app.route("/admin_profile/alta", methods=["POST"])
def alta_producto():
    template_registrar_producto = FormularioRellanarProducto(request.form)


    return redirect(url_for("alta_producto"))


@app.route("/admin_profile/baja", methods=["GET"])
def baja_producto():
    return render_template("bajaproducto.html")


@app.route("/admin_profile/ver", methods=["GET"])
def ver_productos():
    return render_template("verproductos.html")


@app.route("/", methods=["GET"])
def home():
    # elegir el producto de la lista de productos corte ingles
    producto = {
        "fecha_add": "",
        "nombre": "",
        "imagen": "",
        "url": "",
        "h": 400,
        "w": 200,

    }
    #

    return render_template("index.html")


if __name__ == '__main__':
    app.run("127.0.0.1", 5000, debug=True)

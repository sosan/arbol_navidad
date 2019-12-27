"""
 APLICACION QUE SORTEA REGALOS DEL CORTE INGLES
 CON ADMIN DONDE INTRODUCIR LOS DATOS.
 CON ADMIN CON SCRAPPING AUTOMATIZADO

    NO sigue el modelo MVC 100% porque es demasiado corto,
    la parte de interfaz ManagerLogica.py
"""

from flask import Flask
from flask import session
from flask import abort
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_bootstrap import Bootstrap
import uuid
from ModuloLogica.ManagerLogica import ManagerLogica
from TemplateFormularios.Admin import *

# inicializacion e instanciacion
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "sescreto"
managerlogica = ManagerLogica()


@app.route("/admin", methods=["GET"])
def home_admin():
    return render_template("admin_login.html")


@app.route("/admin_profile", methods=["GET"])
def admin_profile():
    return render_template("admin_profile.html")


@app.route("/admin_profile/muchos_alta", methods=["GET"])
def alta_muchos_productos():
    template_registrar_producto = FormularioRellanarMuchosProductos(request.form)
    registrado_ok = False

    if "registrado_ok" in session and "nombreproducto" in session and "resultados" in session:
        registrado_ok = session["registrado_ok"]
        urlsinsertadas = session.pop("resultados")
        if registrado_ok == True:
            session["registrado_ok"] = False

        return render_template("altamuchosproductos.html", formulario=template_registrar_producto, ok=registrado_ok,
                               nombreproducto=session["nombreproducto"], urlsinsertadas=urlsinsertadas)

    return render_template("altamuchosproductos.html", formulario=template_registrar_producto, ok=registrado_ok,
                           nombreproducto="")


@app.route("/admin_profile/muchos_alta", methods=["POST"])
def recibirdatos_alta_muchos_productos():
    if "urlproducto" in request.form and "nombreproducto" in request.form:
        template_registrar_producto = FormularioRellanarMuchosProductos(request.form)
        if template_registrar_producto.validate():
            ok, resultados = managerlogica.crearmuchosproductos(request.form["nombreproducto"],
                                                                request.form["urlproducto"]
                                                                )
            session["resultados"] = resultados
            if ok == True:
                session["registrado_ok"] = True
                session["nombreproducto"] = request.form["nombreproducto"]
            else:
                session["registrado_ok"] = False

    return redirect(url_for("alta_muchos_productos"))


@app.route("/admin_profile/alta", methods=["GET"])
def alta_producto():
    template_registrar_producto = FormularioRellanarProducto(request.form)
    registrado_ok = False

    if "registrado_ok" in session and "nombreproducto" in session:
        registrado_ok = session["registrado_ok"]
        if registrado_ok == True:
            session["registrado_ok"] = False

            return render_template("altaproducto.html", formulario=template_registrar_producto, ok=registrado_ok,
                                   nombreproducto=session["nombreproducto"])

    return render_template("altaproducto.html", formulario=template_registrar_producto, ok=registrado_ok,
                           nombreproducto="")


@app.route("/admin_profile/alta", methods=["POST"])
def recibirdatos_alta_producto():
    if request.method == "GET":
        return redirect(url_for("alta_producto"))

    template_registrar_producto = FormularioRellanarProducto(request.form)

    if template_registrar_producto.validate():
        ok = managerlogica.crearproducto(request.form["nombreproducto"],
                                         request.form["urlproducto"]
                                         )
        if ok == True:
            session["registrado_ok"] = True
            session["nombreproducto"] = request.form["nombreproducto"]
        else:
            session["registrado_ok"] = False

    return redirect(url_for("alta_producto"))


@app.route("/admin_profile/baja", methods=["GET"])
def baja_producto():
    return render_template("bajaproducto.html")


@app.route("/admin_profile/ver", methods=["GET"])
def ver_productos():
    return render_template("verproductos.html")


@app.route("/", methods=["GET"])
def home():
    ip = None
    if "ip" not in session:
        session["ip"] = request.remote_addr
        ip = request.remote_addr
    else:
        ip = session["ip"]

    if managerlogica.get_tiempobloqueo(ip) == False:
        return render_template("abort.html", ip=ip)

    if "id_request" in session:

        id_request = session.pop("id_request")
        id_resultado = session.pop("id_resultado")
        grupo = session.pop("grupo")
        # session.clear()

        id_usuario = session["id_usuario"]
        if managerlogica.get_tiempobloqueo(id_usuario) == False:
            abort(404)

        ok, resultados = managerlogica.getcomprobacion(id_resultado, id_request, grupo)
        if ok == True:
            # hemos acertado
            print("Acertado")
            managerlogica.borrarlistadorequests(id_request)
            return render_template("premio.html", premio=resultados)
        else:
            # hemos fallado
            print("Fallado")
            if not resultados:
                managerlogica.borrarlistadorequests(id_request)

            return render_template("index.html",
                                   productosprincipales=resultados,
                                   maxproductosprincipales=len(resultados),
                                   id_request=id_request
                                   )

    # creamos un usuario para ese request

    id_request = str(uuid.uuid4())

    productosprincipales = managerlogica.getproductos(cantidadproductos=3, productosrelleno=3, id_request=id_request)
    if productosprincipales is not None:
        return render_template("index.html",
                               productosprincipales=productosprincipales,
                               maxproductosprincipales=len(productosprincipales),
                               id_request=id_request
                               )

    return render_template("index.html")


@app.route("/tempruta", methods=["POST"])
def recibirproductoseleccionado():
    if "id_resultado" in request.form and "id_request" in request.form:
        try:
            id_resultado = int(request.form["id_resultado"])
        except ValueError:
            raise Exception("Conversion fallida {0}".format(request.form["id_resultado"]))

        session["id_request"] = request.form["id_request"]
        session["id_resultado"] = id_resultado
        session["grupo"] = request.form["grupo"]

    return redirect(url_for("home"))  # __METHOD_OVERRIDE__='POST',


@app.route("/reset", methods=["POST", "GET"])
def reset_tiempo():
    session.clear()
    managerlogica.reset_tiempo(request.form["ip"])
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run("127.0.0.1", 5000, debug=True)

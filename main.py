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
    if "email" in session and "password" in session:
        # comprobar que este correcto
        return redirect(url_for("admin_profile"))

    context = {
        "templatelogin": FormularioLogin(),
        "intentos": 1,
        "suspendido": False
    }

    formulariologin = FormularioLogin(request.form)
    return render_template("admin_login.html", formulario=formulariologin)


@app.route("/admin", methods=["POST"])
def recibir_login_admin():
    formulariologin = FormularioLogin(request.form)
    if formulariologin.validate():
        ok = managerlogica.comprobaradmin(request.form["emailLogin"], request.form["passwordLogin"])
        if ok == True:
            # pa delante
            session["email"] = request.form["emailLogin"]
            session["password"] = request.form["passwordLogin"]

            return redirect(url_for("admin_profile"))
        else:
            # 3 intentos y pa casa
            pass

    return redirect(url_for("home_admin"))


@app.route("/admin_profile", methods=["GET"])
def admin_profile():
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

    return render_template("admin_profile.html")


@app.route("/admin_profile/muchos_alta", methods=["GET"])
def alta_muchos_productos():
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

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
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

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
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

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
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

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


# @app.route("/admin_profile/baja", methods=["GET"])
# def baja_producto():
#
#     if "email" not in session and "password" not in session:
#         return redirect(url_for("home_admin"))
#
#     return render_template("bajaproducto.html")


@app.route("/admin_profile/ver", methods=["GET"])
def ver_productos():
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

    resultados = managerlogica.getallproductos()

    return render_template("verproductos.html", resultados=resultados, maxresultados=len(resultados))


@app.route("/admin_profile/opcion", methods=["POST"])
def opciones():
    ok = comprobaremailpassword()
    if ok == False:
        return redirect(url_for("home_admin"))

    print("opciones")
    if "opcion" in request.form:
        opcion = request.form["opcion"]
        if opcion == "guardar":
            managerlogica.updateproducto(request.form["id"], request.form["nombreproducto"],
                                         request.form["urlproducto"])
        elif opcion == "borrar":
            managerlogica.deleteproducto(request.form["id"])

    return redirect(url_for("ver_productos"))


@app.route("/", methods=["GET"])
def home():
    if "id_request" in session:

        id_request = session.pop("id_request")
        id_resultado = session.pop("id_resultado")
        grupo = session.pop("grupo")
        # session.clear()

        ok, resultados = managerlogica.getcomprobacion(id_resultado, id_request, grupo)
        managerlogica.borrarlistadorequests(id_request)
        if ok == True:
            # hemos acertado
            print("Acertado")
            bloquearip(request.remote_addr)

            return render_template("premio.html", premio=resultados)
        else:
            # hemos fallado
            print("Fallado")
            if not resultados:
                bloquearip(request.remote_addr)
                # ip = None
                # if "ip" not in session:
                #     session["ip"] = request.remote_addr
                #     ip = request.remote_addr
                # else:
                #     ip = session["ip"]
                #
                # managerlogica.set_tiempobloqueo(ip)
                return render_template("abort.html", ip=request.remote_addr)

            return render_template("index.html",
                                   productosprincipales=resultados,
                                   maxproductosprincipales=len(resultados),
                                   id_request=id_request
                                   )

    ip = None
    if "ip" not in session:
        session["ip"] = request.remote_addr
        ip = request.remote_addr
    else:
        ip = session["ip"]

    if managerlogica.get_tiempobloqueo(ip) == False:
        return render_template("abort.html", ip=ip)

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
            id_resultado = int(float(request.form["id_resultado"]))
        except ValueError:
            raise Exception("Conversion fallida {0}".format(request.form["id_resultado"]))

        session["id_request"] = request.form["id_request"]
        session["id_resultado"] = id_resultado
        session["grupo"] = request.form["grupo"]

    return redirect(url_for("home"))  # __METHOD_OVERRIDE__='POST',


@app.route("/reset", methods=["POST", "GET"])
def reset_tiempo():
    session.clear()
    if request.method == "POST":
        managerlogica.reset_tiempo(request.form["ip"])
    else:
        managerlogica.reset_tiempo(request.remote_addr)
    return redirect(url_for("home"))


def comprobaremailpassword():
    if "email" not in session or "password" not in session:
        return False
    elif "email" in session and "password" in session:
        ok = managerlogica.comprobaradmin(session["email"], session["password"])
        return ok
    return False


def bloquearip(ip_remota):
    if "ip" not in session:
        session["ip"] = ip_remota
        managerlogica.set_tiempobloqueo(ip_remota)
    else:
        managerlogica.set_tiempobloqueo(session["ip"])


if __name__ == '__main__':
    app.run("127.0.0.1", 5000, debug=True)

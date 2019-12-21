from wtforms import Form
from wtforms import StringField
from wtforms import validators
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import ValidationError

from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired
import re


# from mysql.manager import sqlman
# from nosql.manager import redisman
# from mysql.manager import ExisteEnum
#
# existeenum = ExisteEnum()

class FormularioRellanarProducto(Form):
    nombreproducto = StringField(label="Nombre Producto:", validators=[
        validators.data_required(message="Este campo es requerido"),
    ], description="Nombre Producto")


    urlproducto =  URLField(label="URL Producto:", validators=[
        validators.data_required(message="Este campo es requerido"),
    ], description="Url Producto")

    urlimagenproducto = URLField(label="URL IMAGEN Producto:", validators=[
        validators.data_required(message="Este campo es requerido"),
    ], description="Url Imagen Producto")


class FormularioLogin(Form):
    emailLogin = EmailField("email: ", validators=[
        validators.data_required(message="Este campo es requerido"),
        validators.email("Ingrese un email correcto")
        # ,comprobarRedisLogin  # nosql
        # comprobarDBCorreoLogin  # mysql

    ], description="Email")

    emailLoginhidden = HiddenField("email")

    passwordLogin = PasswordField("Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.length(
            min=3, max=10, message="Clave entre 3 y 10 caracteres")
    ], description="Password")

    confirmPasswordLogin = PasswordField("Repite Password: ", validators=[
        validators.data_required(
            message="Estas obligado a rellenar este campo"),
        validators.equal_to("passwordLogin", "Las contraseñas deben ser iguales")

    ], description="Repite Password")

import locale
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class ManagerMongoDb:
    def __init__(self):
        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.cursor: Collection = None
        self.prefixeditado = "(EDITADO)"

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.cursor = self.db[coleccion]
        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    def getAllNotas(self):
        datos = list(self.cursor.find({}).sort("fecha", direction=-1))

        if len(datos) > 0:
            return datos
        return None

    def crearproducto(self, nombreproducto, urlproducto, urlimagenproducto):
        fecha = datetime.utcnow()

        ok = self.cursor.insert_one(
            {"nombreproducto": nombreproducto, "urlproducto": urlproducto, "urlimagenproducto": urlimagenproducto,
             "fecha": fecha, "fecha_mod": fecha, "modificado": False})
        if ok.inserted_id != None:
            return True
        return False

    def borrarnota(self, id):
        ok = self.cursor.delete_one({"_id": ObjectId(id)})
        if ok.deleted_count > 0:
            return 1
        return 0

    def modificarnota(self, id, titulo, nota):

        resultados = self.cursor.find_one({"_id": ObjectId(id)})

        if len(resultados) > 0:
            fecha_current = datetime.utcnow()
            if resultados["fecha_mod"] < fecha_current:

                contenido = {
                    "titulo": titulo,
                    "nota": nota,
                    "fecha_mod": fecha_current,
                    "modificado": True
                }

                ok = self.cursor.update_one({"_id": ObjectId(id)}, {"$set": contenido})
                if ok.modified_count > 0:
                    return True
        return False


managermongo = ManagerMongoDb()

managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net/test?retryWrites=true&w=majority",
                      db="arbol", coleccion="productos")

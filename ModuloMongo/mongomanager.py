import locale
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
import ModuloWeb.managerWeb  # evitar circle imports


class ManagerMongoDb:
    def __init__(self):
        self.managerweb = ModuloWeb.managerWeb.ManagerWeb()
        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.cursor: Collection = None
        self.cursorAyudas: Collection = None

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.cursor = self.db[coleccion]
            self.cursorAyudas = self.db["ayudas"]
        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    def getAllNotas(self):
        datos = list(self.cursor.find({}).sort("fecha", direction=-1))

        if len(datos) > 0:
            return datos
        return None

    def getid_autoincremental(self, idcontador, keyaumentar):
        id_autoincremental = self.cursorAyudas.find_one_and_update(
            {"_id": idcontador},
            {"$inc": {keyaumentar: 1}},
            projection={"_id": False},
            upsert=True,
            return_document=ReturnDocument.AFTER

        )
        if id_autoincremental is None:
            return False

        return True, id_autoincremental["cantidadproductos"]

    def altaproducto(self, id_auto, fecha, nombreproducto, urlproducto, urlimagenproducto, h, v):

        ok = self.cursor.insert_one(
            {
                "_id": id_auto,
                "fecha": fecha,
                "fecha_mod": fecha,
                "nombreproducto": nombreproducto,
                "urlproducto": urlproducto,
                "urlimagenproducto": urlimagenproducto,
                "h": h,
                "v": v,
                "modificado": False
            }
        )
        if ok.inserted_id != None:
            return True
        return False

    def borrarnota(self, id):
        ok = self.cursor.delete_one({"_id": ObjectId(id)})
        if ok.deleted_count > 0:
            return 1
        return 0

    def modificarnota(self, ide, titulo, nota):

        resultados = self.cursor.find_one({"_id": ObjectId(ide)})

        if len(resultados) > 0:
            fecha_current = datetime.utcnow()
            if resultados["fecha_mod"] < fecha_current:

                contenido = {
                    "titulo": titulo,
                    "nota": nota,
                    "fecha_mod": fecha_current,
                    "modificado": True
                }

                ok = self.cursor.update_one({"_id": ObjectId(ide)}, {"$set": contenido})
                if ok.modified_count > 0:
                    return True
        return False

    def getcantidadproductos(self):
        resultados = self.cursorAyudas.find_one({"_id": "contador"}, {"_id": False})
        if resultados == None:
            return False
        return True, resultados["cantidadproductos"]

    def getproductosbyid(self, ides):

        patron = []
        for i in range(0, len(ides)):
            patron.append({"_id": ides[i]})

        ok, resultados = self.cursor.find(patron)
        if ok == False:
            return False

        return resultados



managermongo = ManagerMongoDb()

managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net/test?retryWrites=true&w=majority",
                      db="arbol", coleccion="productos")

import locale
import uuid

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class ManagerMongoDb:
    def __init__(self):

        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.cursor: Collection = None
        self.cursorAyudas: Collection = None
        self.cursorListadoRequests: Collection = None
        self.cursorBloqueos: Collection = None

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.cursor = self.db[coleccion]
            self.cursorAyudas = self.db["ayudas"]
            self.cursorListadoRequests = self.db["listadorequests"]
            self.cursorBloqueos = self.db["bloqueos"]

        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    #
    # def getAllNotas(self):
    #     datos = list(self.cursor.find({}).sort("fecha", direction=-1))
    #
    #     if len(datos) > 0:
    #         return datos
    #     return None

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
                "id_auto": id_auto,
                "fecha": fecha,
                "fecha_mod": fecha,
                "nombreproducto": nombreproducto,
                "urlproducto": urlproducto,
                "urlimagenproducto": urlimagenproducto,
                "h": h,
                "v": v,
                "principal": False,
                "modificado": False
            }
        )
        if ok.inserted_id != None:
            return True
        return False

    # def borrarnota(self, id):
    #     ok = self.cursor.delete_one({"_id": ObjectId(id)})
    #     if ok.deleted_count > 0:
    #         return 1
    #     return 0

    def getcantidadproductos(self):
        resultados = self.cursorAyudas.find_one({"_id": "contador"}, {"_id": False})
        if resultados == None:
            return False
        return True, resultados["cantidadproductos"]

    def getproductosbyid(self, ides):
        patron = {"id_auto": {"$in": ides}}
        resultados = list(self.cursor.find(patron).sort("id_auto", 1))
        if len(resultados) <= 0:
            return None
        return resultados

    def setrequest(self, resultados, id_request: str):

        list_temp = []
        for i in range(0, len(resultados)):

            dict_temp = {
                "id_request": id_request,
                "id_auto": resultados[i]["id_auto"],
                "fecha": resultados[i]["fecha"],
                "fecha_mod": resultados[i]["fecha_mod"],
                "nombreproducto": resultados[i]["nombreproducto"],
                "urlproducto": resultados[i]["urlproducto"],
                "urlimagenproducto": resultados[i]["urlimagenproducto"],
                "h": resultados[i]["h"],
                "v": resultados[i]["v"],
                "modificado": resultados[i]["modificado"]
            }

            if "principal" in resultados[i]:
                dict_temp["principal"] = resultados[i]["principal"]
            else:
                dict_temp["principal"] = False
            list_temp.append(dict_temp)

        ok = self.cursorListadoRequests.insert_many(list_temp)
        if len(ok.inserted_ids) != len(resultados):
            return None
        return True

    def getcomprobacion(self, id_resultado, id_request):
        resultados = list(self.cursorListadoRequests.find({"id_request": id_request}).sort(key_or_list="id_auto",
                                                                                           direction=1))
        return resultados

    def borrarrrequests(self, id_requests):
        ok = self.cursorListadoRequests.delete_many({"id_request": id_requests})
        return ok

    def updaterequest(self, id_request, list_id_auto):

        ok = self.cursorListadoRequests.update_many(
            {"id_request": id_request, "id_auto": {'$in': list_id_auto}}, {'$set': {"modificado": True}}
        )
        if ok.modified_count == 3:
            return True
        return False

    def getoportunidades(self, id_request):
        ok = list(self.cursorListadoRequests.find({"id_request": id_request, "modificado": False}))
        if len(ok) > 0:
            return True
        return False

    def reset_tiempo(self, ip):
        resultado = self.cursorBloqueos.find_one({"ip": ip})
        if resultado != None:
            tiempo_request_24h = resultado["tiempo_request"] - timedelta(hours=25)
            ok = self.cursorBloqueos.update_one({"ip": ip},
                                                {"$set": {"tiempo_request": tiempo_request_24h}})
            if ok.modified_count == 1:
                return True
        return False

    def get_tiempobloqueo(self, ip):
        ok = self.cursorBloqueos.find_one({"ip": ip})
        if ok != None:
            return ok
        return None

    def set_tiempobloqueo(self, ip):
        fecha = datetime.utcnow() + timedelta(hours=24)
        resultado = self.cursorBloqueos.find_one({"ip": ip})
        if resultado == None:
            ok = self.cursorBloqueos.insert_one({"tiempo_request": fecha, "ip": ip})
            if ok.inserted_id != None:
                return True
        else:
            ok = self.cursorBloqueos.update_one({"ip": ip},
                                                {"$set": {"tiempo_request": fecha}})

        return False


managermongo = ManagerMongoDb()
managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net/test?retryWrites=true&w=majority",
                      db="arbol", coleccion="productos")

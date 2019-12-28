from datetime import datetime
from datetime import timedelta
import ModuloWeb.managerWeb
import ModuloMongo.mongomanager
import random


class ManagerLogica:
    def __init__(self):
        self.managerweb = ModuloWeb.managerWeb.ManagerWeb()
        self.managermongo = ModuloMongo.mongomanager.managermongo

    def crearproducto(self, nombreproducto, urlproducto):
        fecha = datetime.utcnow()

        ok, urlimagenproducto, ht, vt = self.managerweb.getProducto(urlproducto)
        if ok == False:
            return False
        try:
            h = int(int(ht) // 4)
            v = int(int(vt) // 4)
        except ValueError:
            raise Exception("No se ha podido convertir en int ht={0} vt={1}".format(ht, vt))

        ok, id_autoincremental = self.managermongo.getid_autoincremental("contador", "cantidadproductos")
        if ok == False:
            return False

        ok = self.managermongo.altaproducto(id_autoincremental, fecha,
                                            nombreproducto, urlproducto, urlimagenproducto, h, v)

        return ok

    def crearmuchosproductos(self, nombregeneralproductos, strproductos):
        listado_resultados = []
        insertadostodos = True
        listproductos = strproductos.splitlines()
        for i in range(0, len(listproductos)):
            ok = self.crearproducto(nombregeneralproductos, listproductos[i])
            print("Creado")
            listado_resultados.append((ok, listproductos[i]))
            if ok == False:
                insertadostodos = False

        return insertadostodos, listado_resultados

    def getallproductos(self):
        resultados = self.managermongo.getallproductos()
        return resultados

    def getproductos(self, cantidadproductos, productosrelleno, id_request):
        ok, maxcantidad = self.managermongo.getcantidadproductos()
        if ok == False:
            return False

        # 3 * 3
        totalmatriz = cantidadproductos * productosrelleno

        setids = set()

        while totalmatriz > len(setids):
            setids.add(random.randint(1, maxcantidad))

        listadoids = list(setids)

        resultados = self.managermongo.getproductosbyid(listadoids)
        if resultados == None:
            return None
        # desordenador lista resultados
        # random.shuffle(resultados)
        # resultados = random.sample(resultados, len(resultados))
        # sorted(resultados,  key=lambda elemento: elemento["id_auto"])  # ordenados por id_auto

        # elegimos 1 como producto principal
        rnd = random.randint(0, 2)
        resultados[rnd]["principal"] = True

        rnd = random.randint(3, 5)
        resultados[rnd]["principal"] = True

        rnd = random.randint(6, 8)
        resultados[rnd]["principal"] = True

        ok = self.managermongo.setrequest(resultados, id_request)
        if ok is False:
            return None

        return resultados

    def getcomprobacion(self, id_resultado, id_request, grupo):
        resultados = self.managermongo.getcomprobacion(id_resultado, id_request)
        oportunidades = False
        if len(resultados) > 0:
            for i in range(0, len(resultados)):
                if resultados[i]["id_auto"] == id_resultado:
                    if resultados[i]["principal"] == True:
                        return True, resultados[i]

            resultados = self.setErrores(grupo, resultados, id_request)  # FUNCIONA CORRECTO
            oportunidades = self.managermongo.getoportunidades(id_request)
            if oportunidades == False:
                resultados = []
        return False, resultados

    def borrarlistadorequests(self, id_requests):
        ok = self.managermongo.borrarrrequests(id_requests)
        return ok

    def setErrores(self, grupo, resultados, id_request):
        list_id_auto = []
        if grupo == "0":
            for i in range(0, 3):
                resultados[i]["modificado"] = True
                list_id_auto.append(resultados[i]["id_auto"])
        elif grupo == "1":
            for i in range(3, 6):
                resultados[i]["modificado"] = True
                list_id_auto.append(resultados[i]["id_auto"])
        elif grupo == "2":
            for i in range(6, 9):
                resultados[i]["modificado"] = True
                list_id_auto.append(resultados[i]["id_auto"])
        else:
            raise Exception("Error grupos {0}".format(grupo))

        ok = self.managermongo.updaterequest(id_request, list_id_auto)
        if ok == False:
            raise Exception("no update correcto: {0}".format(id_request))
        return resultados

    def reset_tiempo(self, ip):
        self.managermongo.reset_tiempo(ip)

    def get_tiempobloqueo(self, ip):
        resultado = self.managermongo.get_tiempobloqueo(ip)
        if resultado == None:
            return True
        else:
            if resultado["tiempo_request"] > datetime.utcnow():
                return False
            else:
                return True

    def set_tiempobloqueo(self, ip):
        ok = self.managermongo.set_tiempobloqueo(ip)
        return ok

    def get_tiempobloqueo2(self, ip):
        resultado = self.managermongo.get_tiempobloqueo(ip)
        if resultado != None:
            tiempo_request_mas_24h = resultado["tiempo_request"] + timedelta(hours=24)
            if datetime.utcnow() < tiempo_request_mas_24h:
                return False
            else:
                return True
        else:
            ok = self.managermongo.set_tiempbloqueo(ip)
            return ok

    def updateproducto(self, idproducto, nombreproducto, urlproducto):
        fecha = datetime.utcnow()

        ok, urlimagenproducto, ht, vt = self.managerweb.getProducto(urlproducto)
        if ok == False:
            return False
        try:
            h = int(int(ht) // 4)
            v = int(int(vt) // 4)
        except ValueError:
            raise Exception("No se ha podido convertir en int ht={0} vt={1}".format(ht, vt))

        ok = self.managermongo.updateproducto(fecha, idproducto,
                                              nombreproducto, urlproducto, urlimagenproducto, h, v)

        return ok

    def deleteproducto(self, idproducto):
        ok = self.managermongo.deleteproducto(idproducto)
        return ok

    def comprobaradmin(self, usuario, password):
        ok = self.managermongo.comprobaradmin(usuario, password)
        return ok

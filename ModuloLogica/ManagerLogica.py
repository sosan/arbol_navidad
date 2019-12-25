from datetime import datetime
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
        random.shuffle(resultados)
        # resultados = random.sample(resultados, len(resultados))

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

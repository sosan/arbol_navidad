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

    def getproductos(self, cantidadproductos, productosrelleno):
        ok, maxcantidad = self.managermongo.getcantidadproductos()
        # 3 * 3
        cantidadproductos = cantidadproductos * productosrelleno
        if ok == False:
            return False

        listaids = []
        for i in range(0, cantidadproductos):
            listaids.append(random.randint(0, maxcantidad))

        ok, resultados = self.managermongo.getproductosbyid(listaids)
        if ok == False:
            return False

        return resultados
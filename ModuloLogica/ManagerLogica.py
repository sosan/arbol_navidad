from datetime import datetime
import ModuloWeb.managerWeb
import ModuloMongo.mongomanager


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

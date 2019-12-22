from json import JSONDecodeError
from requests_html import HTMLSession
from datetime import datetime
import json
import math
import doctest
import ModuloMongo.mongomanager  # evitar circle imports


class ManagerWeb:
    def __init__(self):
        # self.dic_meses = {
        #     "enero": 1,  "febrero": 2,  "marzo": 3,  "abril": 4, "mayo": 5, "junio": 6,
        #     "julio": 7, "agosto": 8,  "septiembre": 9,  "octubre": 10,  "noviembre": 11, "diciembre": 12,
        #     1: "enero", 2: "febrero",  3: "marzo",  4: "abril", 5: "mayo",  6: "junio",
        #     7: "julio",  8: "agosto", 9: "septiembre",  10: "octubre", 11: "noviembre", 12: "diciembre"
        # }
        # self.URL_PELICULAS_HD = "https://dontorrent.org/descargar-peliculas/hd"
        # self.URL_SERIES = "https://dontorrent.org/descargar-series"
        # self.URL_GOOGLE = "https://www.google.com/search?q="
        # self.URL_AFINITY = "https://www.filmaffinity.com/es/advsearch2.php?q="
        # self.URL_API_AFINITY = "https://api-filmaffinity.herokuapp.com/api/busqueda/"
        # self.prefix_dontorrent = "https://dontorrent.org"
        self.web = HTMLSession()

        # self.peliculas = None
        # self.series = None

    def getProducto(self, urlproducto):
        producto = self.web.get(urlproducto)
        lista = []
        # demasiado lento, quizas por ruta mas rapido???
        seleccion = "img#product-image-placer"
        urlimagen = list(producto.html.find(seleccion))
        if len(urlimagen) > 0:
            # //sgfm.elcorteingles.es/SGFM/dctm/MEDIA03/201908/23/00125940611046____2__640x640.jpg
            url = urlimagen[0].attrs["src"]
            dimensiones = url.split("__")[3].split(".")[0].split("x")
            return True, url, dimensiones[0], dimensiones[1]
        return False

        #
        # El miércoles día 04 de diciembre
        fechas = list(producto.html.find(seleccion))
        #fechas[i].links
        # selecciond = "body > div.container > div.row > div.col-lg > div.noticias > " \
        #              "div.position-relative > div.card.shadow.noticia > div.card-body > div.noticiasContent > " \
        #              "div.text-center"
        #
        # links = list(producto.html.find(selecciond))

        # for i in range(0, len(fechas)):
        #     fecha = self.getfechas(fechas[i].text)
        #     lastfecha = managermongo.getLastFecha()
        #     # if fecha > lastfecha:
        #     #     pass
        #     datos = self.getdetail_datos(list(fechas[i].links), fecha)
        #
        #     lista.append(datos)

        # return lista

    # def getfechas(self, fecha):
    #     fechasplits = fecha.split(" ")
    #
    #     dia = int(fechasplits[3])
    #     mes = self.dic_meses[fechasplits[5].lower()]
    #
    #     fecha = datetime(2019, mes, dia)
    #     return fecha

    # def getdetail_datos(self, links, fecha):
    #     lista = []
    #     for i in range(0, len(links)):
    #         titulo = self.gettitulo(links[i])
    #         imagen = self.getimagen(titulo)
    #         resultado = managermongo.encontrarTituloImagen(titulo, imagen)
    #         if resultado == False:
    #             dic = {
    #                 "titulo": titulo,
    #                 "link": self.prefix_dontorrent + links[i],
    #                 "imagen": imagen,
    #                 "fecha": fecha
    #             }
    #             managermongo.insertarurls(dic)
    #             lista.append(dic)
    #
    #     return lista
    #
    # def gettitulo(self, tituloraw):
    #     """
    #     >>> a = "/peli-descargar-torrent-21385-Annabelle-vuelve-a-casa.html"
    #     >>> a = "/peli-descargar-torrent-21472-Mascotas-2-4K.html"
    #     >>> b = a.split("-")
    #     >>> titulo = gettitulo(splits=b)
    #     >>> print(titulo)
    #     Mascotas 2
    #
    #     """
    #     t = tituloraw.replace(".", "").replace("html", "").replace("4K", "").replace("3D", "")
    #     splits = t.split("-")
    #     titulo = []
    #     for o in range(4, len(splits)):
    #         if splits[o].count(".") == 0:
    #             titulo.append(splits[o])
    #         else:
    #             titulo.append(splits[o].split(".")[0])
    #
    #     titulo = " ".join(titulo)
    #     return titulo
    #
    # def getimagen_google(self, titulo):
    #     google = self.web.get(self.URL_GOOGLE + titulo)
    #     seleccion = "/html/body/div[6]/div[3]/div[10]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/a/g-img"
    #     fotos = google.html.xpath(seleccion)
    #     if len(fotos) > 0:
    #         f = fotos[0].html
    #         foto = f.split('"')[15]
    #         return foto
    #     else:
    #         return None
    #
    # def getimagen(self, titulo):
    #     apiafinity = self.web.get(self.URL_API_AFINITY + titulo)
    #     print(titulo)
    #     try:
    #         datos = json.loads(apiafinity.html.text)
    #     except JSONDecodeError:
    #         raise Exception("Excepcion {0}=>{1}".format(titulo, apiafinity.html.text))
    #
    #     if len(datos) > 0:
    #         web = datos[0]["id"]
    #         webafini = self.web.get(web + ".html")
    #         seleccion = "div#movie-main-image-container"
    #         f = webafini.html.find(seleccion)
    #         if len(f) > 0:
    #             urlfotos = list(f[0].links)
    #             if len(urlfotos) > 0:
    #                 urlfoto = urlfotos[0]
    #                 return urlfoto
    #     return None
    #
    # def getSeries(self):
    #     self.series = self.web.get(self.URL_SERIES)
    #     return self.series


############################

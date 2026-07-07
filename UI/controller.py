import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def readShapes(self):
        res = []
        for s in self._model.getShapes():
            res.append(ft.dropdown.Option(s))
        return res

    def handle_graph(self, e):
        for minLat, maxLat, lonMin, lonMax in self._model.estremi():
            minLat = float(minLat)
            maxLat = float(maxLat)
            lonMin = float(lonMin)
            lonMax = float(lonMax)

        lat = self._view.txt_latitude.value
        lon = self._view.txt_longitude.value
        if lat is None or lon is None:
            self._view.txt_result1.controls.append(ft.Text("Inserire una longitudine e una latitudine", color="red"))
            self._view.update_page()
            return
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            self._view.txt_result1.controls.append(ft.Text("Inserire un numeri validi", color="red"))
            self._view.update_page()
            return
        if not (float(minLat) <= lat <= float(maxLat)):
            self._view.txt_result1.controls.append(ft.Text(f"La latitudine deve essere compresa tra"
                                                           f" {minLat} e {maxLat}", color="red"))
            self._view.update_page()
            return
        if not( float(lonMin) <= lon <= float(lonMax)):
            self._view.txt_result1.controls.append(ft.Text(f"La longitudine deve essere compresa tra"
                                                           f" {lonMin} e {lonMax}", color="red"))
            self._view.update_page()
            return

        shape = self._view.ddshape.value
        if shape is None :
            self._view.txt_result1.controls.append(ft.Text("Selezionare una forma (shape)", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(lat,lon, shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}", color="green"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}", color="green"))

        nodi_con_gradi , lista_pesati = self._model.getDettagli()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi con grado maggiore", color="blue"))

        for n, grado in nodi_con_gradi:
            self._view.txt_result1.controls.append(ft.Text(f"{n} --> degree={grado}"))

        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi con peso maggiore", color="blue"))

        for u,v,peso in lista_pesati:
            self._view.txt_result1.controls.append(ft.Text(f"{u} - {v}     peso= {peso}"))
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        try:
            percorso, punteggio = self._model.bestPercorso()
        except Exception as ex:
            self._view.txt_result2.controls.append(
                ft.Text(f"Errore nel calcolo del percorso: {ex}", color="red"))
            self._view.update_page()
            return

        if not percorso:
            self._view.txt_result2.controls.append(
                ft.Text("Nessun percorso valido trovato", color="red"))
            self._view.update_page()
            return

        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio totale: {punteggio}", color="green"))
        self._view.txt_result2.controls.append(
            ft.Text("Percorso:", color="blue"))

        for stato in percorso:
            try:
                densita = stato.Population / stato.Area
            except (ZeroDivisionError, TypeError):
                densita = "N/D"
            self._view.txt_result2.controls.append(
                ft.Text(f"{stato}  -  densità: {densita}"))

        self._view.update_page()


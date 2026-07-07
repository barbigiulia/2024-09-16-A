
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.grafo = nx.Graph()

    def estremi(self):
        return DAO.MineMax()

    def getShapes(self):
        return DAO.getShapes()


    def buildGraph(self, lat, long,shape):
        nodi=[]
        for state in DAO.getNodes(lat, long, shape):
            nodi.append(state)
        self.grafo.add_nodes_from(nodi)
        self.addEdges(lat, long,shape)


    def addEdges(self, lat, long, shape):
        avvistamenti = DAO.getAvvistamenti(lat, long, shape)
        state_to_neighbours = {}    #idState = [idState1, idState2....]
        durate = {}   #idState = {totDurata degli avvistamenti in questo stato}
        for id, lista, duration in avvistamenti:
            if id not in state_to_neighbours:
                lista_vicini = []
                for v in lista.split(" "):
                    lista_vicini.append(v.strip())
                state_to_neighbours[id] = lista_vicini
            if id not in durate:
                durate[id] =0
            durate[id] += duration

        nodi = list(self.grafo.nodes)
        for i in range(len(nodi)):
            for j in range(i+1, len(nodi)):
                state1_ID = nodi[i].id
                state2_ID = nodi[j].id

                if (self.sonoVicini(state1_ID, state2_ID, state_to_neighbours))==True:
                    peso1 = durate.get(state1_ID,0)
                    peso2 = durate.get(state2_ID,0)
                    self.grafo.add_edge(nodi[i], nodi[j], weight=peso1 + peso2)


    def sonoVicini(self, state1, state2, state_to_neighbours):
        for id in state_to_neighbours:
            if id == state1:
                for vicino in state_to_neighbours[id]:
                    if vicino == state2:
                        return True
        return False

    def getNumNodi(self):
        return len(self.grafo.nodes)
    def getNumArchi(self):
        return len(self.grafo.edges)



    def getDettagli(self):
        res = []
        for nodo in self.grafo.nodes:
            grado = self.grafo.degree(nodo)
            res.append((nodo, grado))
        res.sort(key=lambda x: x[1], reverse=True)
        archi=[]
        for u,v, data in self.grafo.edges(data=True):
            archi.append((u,v,data["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)

        return res[:5], archi[:5]



    # punteggio da massimizzare = totPesi_archi / tot_distanza_percorsa
    # nodo successivo ha una densità di popolazione strett. crescente (population/area)

    def bestPercorso(self):
        self._bestPath = []
        self._bestScore = 0
        for nodo in self.grafo.nodes:
            densita = nodo.Population/nodo.Area
            self._ricorsione(nodo, [nodo], densita )
        return self._bestPath, self._bestScore

    def _ricorsione(self, nodoCorrente, parziale, densitaUltima):
        if len(parziale) > 1:
            punteggio = self.calcolaPunteggio(parziale)
            if punteggio > self._bestScore:
                self._bestScore = punteggio
                self._bestPath = list(parziale)

        for vicino in self.grafo.neighbors(nodoCorrente):
            if vicino not in parziale:
                densitaVicino = vicino.Population/vicino.Area
                if densitaVicino > densitaUltima:
                    parziale.append(vicino)
                    self._ricorsione(vicino, parziale,  densitaVicino)
                    parziale.pop()

    def calcolaPunteggio(self, parziale):
        # itera sulle coppie consecutive del percorso
        peso = 0
        distanza = 0
        for i in range(len(parziale) - 1):
            nodo = parziale[i]
            vicino = parziale[i + 1]
            peso += self.grafo[nodo][vicino]["weight"]
            distanza += nodo.distance_HV(vicino)
        if distanza == 0:
            return 0
        return peso / distanza

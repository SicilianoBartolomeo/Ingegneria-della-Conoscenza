import json
import requests
import osmnx as ox
import networkx as nx
import urllib.parse
from prettytable import PrettyTable

class Navigator:
    def __init__(self):
        self.G = ox.graph_from_address(
        "Via Capruzzi, Bari, Italy",
        dist=3500,
        network_type="drive",
        truncate_by_edge=True,
        )

    def askDestination(self):
        with open('Resources\meccanici.json', 'r') as f:
            data = json.load(f)

        x = PrettyTable()
        x.field_names = ["Id", "Nome", "Indirizzo"]
        for d in data:
            x.add_row([d["_id"], d["nome"], d["indirizzo"]])

        print("Ecco una lista delle officine di Bari: \n")
        print(x)

        flag = False
        while(not(flag)):
            userInput = ''
            userInput = input("Inserire l'id dell'officina desiderata --> ")
            try:
                id = int(userInput)
                if(id < 1 or id > 13):
                    raise Exception("Errore! Id non valido. L'id deve essere compreso tra 1 e 13\n")
                flag = True
            except (ValueError, Exception) as ex:
                print("Errore! L'id inserito deve essere un intero compreso tra 1 e 13.\n")

        return id

    def askOrigin(self):
        print("\nInserire l'indirizzo da cui vuoi partire nel formato:\n",
        "via, numero, citta' (quest'ultima deve essere Bari).\n",
        "Le virgole non sono obbligatorie ma aiutano nella ricerca di OSM\n",
        "maggiori saranno i dettagli inseriti migliore sara' la precisione della ricerca.")
        address = input("--> ")
        return address

    def askKindOfSearch(self):
        question = "Quale algoritmo vuoi che venga usato per la ricerca del percorso?\n"
        question += "\t(1) algoritmo di ricerca che minimizza la distanza euclidea\n"
        question += "\t(2) algoritmo di Dijkstra\n\t(3) algoritmo A*\n"
        question += "\t(4) tutti e tre i precedenti elencati" 
        print(question)
        flag = False
        while(not(flag)):
            userInput = ''
            userInput = input(" --> ")
            try:
                answer = int(userInput)
                if(answer < 1 or answer > 4):
                    raise Exception()
                flag = True
            except (ValueError, Exception) as ex:
                print("Errore! Risposta non valida. La risposta deve essere un INTERO compreso tra 1 e 4\n")
        return answer

    def getCoordinateFromId(self, id):
        with open('Resources\meccanici.json', 'r') as f:
            data = json.load(f)

        coordinate = []
        for d in data:
            if(d["_id"] == id):
                coordinate.append(d["latitudine"])
                coordinate.append(d["longitudine"])
        return coordinate

    def getCoordinateFromAddress(self, address):
        #address = 'Via Francesco Campione, 62, 70124 Bari BA'
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

        response = requests.get(url).json()

        coordinate = []
        coordinate.append(float(response[0]["lat"]))
        coordinate.append(float(response[0]["lon"]))
        return coordinate

    def getAllCoordinate(self):
        with open('Resources\meccanici.json', 'r') as f:
            data = json.load(f)

        coordinate = []
        for d in data:
            coordinate.append((d['latitudine'], d['longitudine']))
        return coordinate
    
    def searchNearestMechanic(self):
        minRouteDistance = 0
        minRoute = []

        flag = False
        while(not(flag)):
            try:
                 origin = self.getCoordinateFromAddress(self.askOrigin())
                 flag = True
            except IndexError as ie:
                print("Errore! Localita' non trovata")
        originNode = ox.distance.nearest_nodes(self.G, origin[1], origin[0])

        for c in self.getAllCoordinate():
            pathDistance = 0
            destinationNode = ox.distance.nearest_nodes(self.G, c[1], c[0])
            route = ox.shortest_path(self.G, originNode, destinationNode, weight = 'length')
        
            for distance in ox.utils_graph.get_route_edge_attributes(self.G, route, 'length', minimize_key='length'):
                pathDistance += distance

            if minRouteDistance == 0:
                minRouteDistance = pathDistance
                minRoute = route

            if pathDistance < minRouteDistance:
                minRouteDistance = pathDistance
                minRoute = route
        return minRoute

    #euclidean distance
    def dist(self, a, b):
        x1 = self.G._node[a]['y']
        y1 = self.G._node[a]['x']
        x2 = self.G._node[b]['y']
        y2 = self.G._node[b]['x']

        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def searchMechanic(self):
        flag = False
        while(not(flag)):
            try:
                origin = self.getCoordinateFromAddress(self.askOrigin())
                flag = True
            except IndexError as ie:
                print("Errore! Localita' non trovata")
        destination = self.getCoordinateFromId(self.askDestination())
        origin_node = ox.distance.nearest_nodes(self.G, origin[1], origin[0])
        destination_node = ox.distance.nearest_nodes(self.G, destination[1], destination[0])

        answer = self.askKindOfSearch()
        if (answer == 1):
            #euclidean distance search algorithm
            route = ox.shortest_path(self.G, origin_node, destination_node, weight = 'length')
            fig, ax = ox.plot_graph_route(self.G, route, route_color="c", node_size=0)

        elif (answer == 2):
            #dijkstra search algorithm
            length,route=nx.single_source_dijkstra(self.G,origin_node, destination_node, weight='length')
            fig, ax = ox.plot_graph_route(self.G, route, route_color="c", node_size=0)

        elif (answer == 3):
            #a* search algorithm ----definire funzione euristica
            route = nx.astar_path(self.G, origin_node, destination_node, heuristic=self.dist, weight = 'length')
            fig, ax = ox.plot_graph_route(self.G, route, route_color="c", node_size=0)
            
        elif (answer == 4):
            route = ox.shortest_path(self.G, origin_node, destination_node, weight = 'length')
            length,route2=nx.single_source_dijkstra(self.G,origin_node, destination_node, weight='length')
            route3 = nx.astar_path(self.G, origin_node, destination_node, heuristic=self.dist, weight = 'length')
            print("In celeste: algoritmo che minimizza la distanza euclidea\n"+
            "in blu: algoritmo di Dijkstra\n" + "in rosso: algoritmo A*")
            fig, ax = ox.plot_graph_route(self.G, route, route_color="c", node_size=0)
            fig, ax = ox.plot_graph_route(self.G, route2, route_color="b", node_size=0)
            fig, ax = ox.plot_graph_route(self.G, route3, route_color="r", node_size=0)

        #print(ox.utils_graph.get_route_edge_attributes(G2, route, 'length', minimize_key='length'))

    def askOperation(self):
        exit = False
        while(not(exit)):
            print("Quale operazione vuoi fare?")
            print("\t(1) Cercare il percorso per un meccanico.")
            print("\t(2) Cercare il percorso per il meccanico piu' vicino.")
            print("\t(3) Terminare il programma.")
 
            flag = False
            while(not(flag)):
                userInput = ''
                userInput = input("Inserire il numero dell'operazione da effettuare --> ")
                try:
                    operation = int(userInput)
                    if(operation < 1 or operation > 3):
                        raise Exception()
                    flag = True
                except (ValueError, Exception) as ex:
                    print("Errore! L'input inserito deve essere un intero compreso tra 1 e 3.\n")

            if(operation == 1):
                self.searchMechanic()
            elif(operation == 2):
                minRoute = self.searchNearestMechanic()
                fig, ax = ox.plot_graph_route(self.G, minRoute, route_color="c", node_size=0)
            elif(operation == 3):
                print("Programma terminato.")
                exit = True


def main():
    navigator = Navigator()
    print("=======================================================================")
    print("|                     Benvenuto nel navigatore                        |")
    print("|                                                                     |")
    print("|Puoi trovare il percorso per un meccanico nella citta' di Bari       |")
    print("|attraverso l'uso di algoritmi di ricerca su grafo.                   |")
    print("=======================================================================")
    navigator.askOperation()

if __name__ == '__main__':
    main()

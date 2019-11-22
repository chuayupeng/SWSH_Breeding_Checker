class Pokemon:
    """
    Simple Node class
    """
    def __init__(self, pokemon, eggGroups):
        """
        Constructor
        :param pokemon: Unique pokemon name
        """
        self.pokemon = pokemon          # type String
        self.eggGroups  = eggGroups     # type List[String]
        self.neighbors = []             # type List[Pokemon]
        self.status = 'undiscovered'    # undiscovered | discovered | explored

        self.distance = -1              # shortest distance from source node in shortest path search
        self.previous = None            # previous vertex in shortest path search

    def addNeighbour(self, pokemon):
        """
        Adds a new vertex as an adjacent neighbor of this vertex
        :param pokemon: new Pokemon() to add to self.neighbors
        """
        self.neighbors.append(pokemon)

    def getEggGroups(self):
        
        """
        Returns a list of all egg groups
        :return: list of Strings
        """
        return self.eggGroups
    
    def getNeighbors(self):
        """
        Returns a list of all neighboring pokemon
        :return: list of Pokemon
        """
        return self.neighbors


def shortestPathBFS(pokemon):
    """
    Shortest Path - Breadth First Search
    :param pokemon: the starting graph node
    :return: does not return, changes in place
    """
    if pokemon is None:
        return

    queue = []                                  # our queue is a list with insert(0) as enqueue() and pop() as dequeue()
    queue.insert(0, pokemon)

    while len(queue) > 0:
        current_pokemon = queue.pop()                    # remove the next node in the queue
        next_distance = current_pokemon.distance + 1     # the hypothetical distance of the neighboring node

        for neighbor in current_pokemon.getNeighbors():
            if neighbor.distance == -1 or neighbor.distance > next_distance:    # try to minimize node distance
                neighbor.distance = next_distance       # distance is changed only if its shorter than the current
                neighbor.previous = current_pokemon      # keep a record of previous vertexes so we can traverse our path
                queue.insert(0, neighbor)


def traverseShortestPath(targetmon):
    """
    Traverses backward from target pokemon to source pokemon, storing all encountered pokemon names
    :param targetmon: Pokemon() Our target node
    :return: A list of all pokemon in the shortest path
    """
    vertexes_in_path = []

    while targetmon.previous:
        vertexes_in_path.append(targetmon.pokemon)
        targetmon = targetmon.previous

    return vertexes_in_path


def populateBFS(monDict, typesDict):
    PokemonNodeDict = {}
    for mon in monDict:
        monTypes = monDict[mon]
        PokemonNodeDict[mon] = Pokemon(mon, monTypes)

    for mon in PokemonNodeDict:
        node = PokemonNodeDict[mon]
        for eggGroup in node.getEggGroups():
            for neighbour in typesDict[eggGroup]:
                if neighbour == mon:
                    continue
                else:
                    node.addNeighbour(PokemonNodeDict[neighbour])
            
    return PokemonNodeDict

def main():
    #clean data
    file = open("egggroups.txt", "r")
    lines = file.readlines()
    monDict = {}
    typesDict = {}
    for line in lines:
        monArr = line.split("\t")
        nameSquared = monArr[0]
        name = nameSquared[0:int((len(nameSquared)/2))]
        eggTypes = list(map(lambda x: x.strip(),monArr[1].split("\n")[0].split("/")))
        monDict[name] = eggTypes
        for eggType in eggTypes:
            if typesDict.get(eggType) == None:
                typesDict[eggType] = [name]
            else:
                typesDict[eggType].append(name)
                
    nodeDict = populateBFS(monDict, typesDict)
    source = "Eevee"
    target = "Charmander"
    shortestPathBFS(nodeDict[source])
    pokemon_to_breed = traverseShortestPath(nodeDict[target])
            
main()

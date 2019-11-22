import sys

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

    def getName(self):
        return self.pokemon

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
    
    def getNeighbours(self):
        """
        Returns a list of all neighboring pokemon
        :return: list of Pokemon
        """
        return self.neighbors

    def getPrev(self):
        return self.previous

def shortestPathBFS(pokemon):
    """
    Shortest Path - Breadth First Search
    :param pokemon: the starting graph node
    :return: does not return, changes in place
    """
    if pokemon is None:
        print("(-) Invalid source pokemon, did you check the sword and shield dex cuts?")
        sys.exit(-1)

    queue = []                                  # our queue is a list with insert(0) as enqueue() and pop() as dequeue()
    queue.insert(0, pokemon)

    while len(queue) > 0:
        current_pokemon = queue.pop()                    # remove the next node in the queue
        next_distance = current_pokemon.distance + 1     # the hypothetical distance of the neighboring node
        if next_distance == 0:
            current_pokemon.distance = -2
        for neighbour in current_pokemon.getNeighbours():
            if neighbour.distance == -1 or neighbour.distance > next_distance:    # try to minimize node distance
                neighbour.distance = next_distance       # distance is changed only if its shorter than the current
                neighbour.previous = current_pokemon      # keep a record of previous vertexes so we can traverse our path
                queue.insert(0, neighbour)
            
    

def traverseShortestPath(targetmon):
    """
    Traverses backward from target pokemon to source pokemon, storing all encountered pokemon names
    :param targetmon: Pokemon() Our target node
    :return: A list of all pokemon in the shortest path
    """
    vertexes_in_path = []

    if targetmon is None:
        print("(-) Invalid target pokemon! Did you check the dex cuts?")
        sys.exit(-1)

    while targetmon.previous != None:
        vertexes_in_path.append(targetmon.pokemon)
        targetmon = targetmon.previous
    vertexes_in_path.append(targetmon.pokemon)
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
                elif PokemonNodeDict[neighbour] not in node.getNeighbours():
                    node.addNeighbour(PokemonNodeDict[neighbour])
                else:
                    continue
######## DEBUG
#        print()
#        print(node.getName())
#        print("Neighbours:")
#        for neighbour in node.getNeighbours():
#            print(neighbour.getName())

    return PokemonNodeDict

def main():
    if len(sys.argv) != 3:
        print("(+) usage: python3 %s source_pokemon target_pokemon" % sys.argv[0])
        print("(+) eg. python3 %s eevee charmander" % sys.argv[0])
        sys.exit(-1)
    # clean data
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
#### DEBUG
#    print(typesDict)
#    print(monDict)
    nodeDict = populateBFS(monDict, typesDict)
    source = sys.argv[1].capitalize()
    target = sys.argv[2].capitalize()
    if source in nodeDict.keys() and target in nodeDict.keys():
        shortestPathBFS(nodeDict[source])
        pokemon_to_breed = traverseShortestPath(nodeDict[target])
        seperator = " -> "
        print(seperator.join(list(reversed(pokemon_to_breed))))
    else:
        print("(-) Invalid source or target pokemon! Did you check the dex cuts? Also pst Ditto or Legendaries aren't included for obvious reasons.")
        sys.exit(-1)

if __name__ == "__main__":
    main()

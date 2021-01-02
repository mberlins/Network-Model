import xml.etree.ElementTree as ET


class City:

    def __init__(self, name, id, x, y):
        self.name = name
        self.id = id
        self.x_coor = x
        self.y_coor = y


class Link:

    def __init__(self, name, src, dest, cap, cost):
        self.name = name
        self.source = src
        self.target = dest
        self.capacity = cap
        self.cost = cost


doc = ET.parse(r"C:\Users\Admin\PycharmProjects\NetworkModel\germany50.xml")
root = doc.getroot()

children = []
childrenBis = []
cities = []
links = []
city = []

for child in root:
    children.append(child)

networkStructure = children[0]
demands = children[1]

# wczytywanie węzłów sieci
for child in networkStructure:
    childrenBis.append(child)

nodes = childrenBis[0]
linksBis = childrenBis[1]

i = 1
for child in nodes:
    cities.append(City(child.attrib['id'], i, child[0][0].text, child[0][1].text))
    i = i + 1

for child in linksBis:
    links.append((Link(child.attrib['id'], child[0].text, child[1].text, child[2][0][0].text, child[2][0][1].text)))

for x in cities:
    print(x.id, x.name, x.x_coor, x.y_coor)

for x in links:
    print(x.name, x.source, x.target, x.cost, x.capacity)

# wczytywanie przepływów sieci

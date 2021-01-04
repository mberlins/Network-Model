import xml.etree.ElementTree as ET


class City:

    def __init__(self, name, it, x, y):
        self.name = name
        self.id = it
        self.x_coor = x
        self.y_coor = y


class Link:

    def __init__(self, it, name, src, dest, cap, cost):
        self.id = it
        self.name = name
        self.source = src
        self.target = dest
        self.capacity = cap
        self.cost = cost


class Demand:

    def __init__(self, it, name, src, dest, val):
        self.id = it
        self.name = name
        self.source = src
        self.target = dest
        self.demand_value = val


# loading xml file to the model ########################################################################################
doc = ET.parse(r"C:\Users\Admin\PycharmProjects\NetworkModel\germany50.xml")
root = doc.getroot()

children = []
childrenBis = []
cities = []
links = []
demands = []

for child in root:
    children.append(child)

networkStructure = children[0]
demandsBis = children[1]

for child in networkStructure:
    childrenBis.append(child)

nodes = childrenBis[0]
linksBis = childrenBis[1]

# loading nodes
i = 1
for child in nodes:
    cities.append(City(child.attrib['id'], i, child[0][0].text, child[0][1].text))
    i = i + 1

# loading links
i = 1
for child in linksBis:
    links.append(Link(i, child.attrib['id'], child[0].text, child[1].text, child[2][0][0].text, child[2][0][1].text))
    i = i + 1

# loading demands
i = 1
for child in demandsBis:
    demands.append(Demand(i, child.attrib['id'], child[0].text, child[1].text, child[2].text))
    i = i + 1

for x in cities:
    print(x.id, x.name, x.x_coor, x.y_coor)

for x in links:
    print(x.name, x.source, x.target, x.cost, x.capacity)

for x in demands:
    print(x.id, x.name, x.source, x.target, x.demand_value)

# selecting size of the network ########################################################################################
networkSize = 50  # size of the network
selectedCities = []
selectedLinks = []
selectedDemands = []

for i in range(networkSize):
    selectedCities.append(cities[i])

counter = 1
for i in links:
    for j in selectedCities:
        if i.source == j.name:
            for k in selectedCities:
                if i.target == k.name:
                    i.id = counter
                    counter = counter + 1
                    selectedLinks.append(i)

counter = 0
for i in demands:
    for j in selectedCities:
        if i.source == j.name:
            for k in selectedCities:
                if i.target == k.name:
                    counter = counter + 1
                    i.id = counter
                    selectedDemands.append(i)

print(len(selectedCities), len(selectedLinks), len(selectedDemands))

# writing selected network to a file ###################################################################################
file = open("C:\\Users\\Admin\\PycharmProjects\\NetworkModel\\PP.dat", "w")

file.write("set VERT :=")
for city in selectedCities:
    file.write(" ")
    file.write(str(city.id))

file.write("; \n\n")
file.write("set ARCS :=")
for link in selectedLinks:
    file.write(" ")
    file.write(str(link.id))

file.write("; \n\n")
file.write("set STREAMS :=")
for stream in selectedDemands:
    file.write(" ")
    file.write(str(stream.id))

file.write("; \n\n")
file.write("set VEHICLES := 1 2 3 4")

file.write("; \n\n")
file.write("set DIM := 1 2")

file.write("; \n\n")
file.write("set LOG_FUN := NONE WER PER")

file.write("; \n\n")
file.write("set DELAYS := DELAYSB DELAYS DELAY DELA DEL")

file.write("; \n\n")
for vertex in selectedCities:
    file.write("set ARCSE[")
    file.write(str(vertex.id))
    file.write("] :=")
    for arc in links:
        if arc.source == vertex.name:
            file.write(" ")
            file.write(str(arc.id))
    file.write(";\n")

file.write("\n\n")
for vertex in selectedCities:
    file.write("set ARCSL[")
    file.write(str(vertex.id))
    file.write("] :=")
    for arc in links:
        if arc.target == vertex.name:
            file.write(" ")
            file.write(str(arc.id))
    file.write(";\n")

file.write("\n\n")
file.write("param source :=\n")
for stream in selectedDemands:
    file.write("\t")
    file.write(str(stream.id))
    file.write("\t")
    for city in selectedCities:
        if stream.source == city.name:
            file.write(str(city.id))
            break
    file.write("\n")

file.write(";\n\n")
file.write("param dest :=\n")
for stream in selectedDemands:
    file.write("\t")
    file.write(str(stream.id))
    file.write("\t")
    for city in selectedCities:
        if stream.target == city.name:
            file.write(str(city.id))
            break
    file.write("\n")

file.write(";\n\n")
file.write("param stream_size (tr):")
for stream in selectedDemands:
    file.write("\t")
    file.write(str(stream.id))
file.write(":=\n")

i = 1
while i < 3:
    file.write("\t\t")
    file.write(str(i))
    for stream in selectedDemands:
        file.write("\t")
        value = float(stream.demand_value)
        value = int(value)
        file.write(str(value))
    file.write("\n")
    i = i + 1

file.write(";\n\n")
file.write("param max_delay:=\n")
for stream in selectedDemands:
    file.write("\t")
    file.write(str(stream.id))
    file.write("\t")
    file.write("DELAYSB")
    file.write("\n")

file.write(";\n\n")
file.write("param travel_cost (tr):")                       #TODO obliczanie dlugości łuków, geograficzne ograniczenia dla miast

file.close()

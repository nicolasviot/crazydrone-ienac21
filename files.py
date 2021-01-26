from drone import *
from flight import *
from geometry import *

"""Ce module contient seulement les deux fonctions nécessaires à la lecture et l'écriture de documents. Ces fonctions
sont appelées lors des appuis des boutons Importer et Enregistrer des fenêtres correspondantes.

RQ : une erreur connue est que lors de la lecture d'un fichier, il se peut que les traits soient tracés de façon erronée.
Il suffit de cliquer sur les traits dans le menu déroulant un à un ou de modifier une distance pour 
qu'ils se téléportent à leur emplacement normal. C'est purement un bug graphique, le drone lui a les bonnes informations dès
l'ouverture du document. Nous n'avons pas eu le temps de résoudre ce bug."""

def load(name):
    FILE = "Trajectoires enregistrées/" + name + ".txt"
    liste_trajectoire =[]
    drawing_points = [Point(0,0)]
    drone_plan = []

#Cette fonction est divisée en 2 parties : la première consiste à lire le document texte et à créer plan de vol drone_plan

    with open(FILE, 'r') as f:
        for line in f:
            liste_trajectoire.append(line.strip().split())

    for elt in liste_trajectoire:
        if elt[0] == 'Take_off':
            drone_plan.append(Take_Off(float(elt[1]),float(elt[2])))
        elif elt[0] == 'TRAIT':
            drone_plan.append(Move_Distance(float(elt[1]),float(elt[2]),float(elt[3]),"TRAIT",float(elt[4])))
        elif elt[0] == 'CERCLE':
            drone_plan.append(Circle(float(elt[1]),str(elt[2]),Point(float(elt[3]),float(elt[4])),'CERCLE',float(elt[5])))

    """La deuxième partie consiste, à partir de drone_plan, à créer la liste drawing_points pour ainsi tracer la trajectoire.
    Pour se faire on calcule à chaque nouvel élément le nombre de cercle situé avant lui car les cercles n'ajoutent pas de points.
    Si l'élement est un trait, on ajoute un nouveau point correspondant à l'extrémité de ce trait moins le point
    précédent (c'est pourquoi on doit utiliser un index retranché)."""

    nb_cercle = 0
    for i,elt in enumerate(drone_plan[1:]):
        j = i+1                             #Décalage car on traverse drone_plan[1:] mais l'indice commence à 0
        if elt.type == "CERCLE":
            nb_cercle += 1
        index_retranché = j - nb_cercle

        if i == 0:
            if elt.type == "TRAIT":

                point = Point(float(elt.x_distance),
                              float(elt.y_distance),
                              float(elt.z_distance))
                drawing_points.append(point)

        else :
            if elt.type == "TRAIT":

                point = Point(float(elt.x_distance) - float(drawing_points[index_retranché - 1].x),
                              float(elt.y_distance) - float(drawing_points[index_retranché - 1].y))
                drawing_points.append(point)

    return drawing_points,drone_plan


"""La fonction save crée un document texte à partir du plan de vol récupéré et du nom saisi par l'utilisateur. On a choisi
pour le format des documents que chaque élément est à une ligne différente et tous les attributs d'un élément sont
sur sa ligne, séparés par un espace"""

def save(flight_plan,name):
    with open("Trajectoires enregistrées/" + name + ".txt", "w") as f:
        for elt in flight_plan:

            if elt.type == "Take_off":
                f.write(elt.type + " " +str(elt.distance)  +" " + str(elt.velocity) )
                f.write("\n")
            elif elt.type == "TRAIT":
                f.write(elt.type + " " + str(elt.x_distance) + " " + str(elt.y_distance) + " " +str(elt.z_distance) + " " + str(elt.velocity))
                f.write("\n")
            elif elt.type == "CERCLE":
                f.write(elt.type + " " + str(elt.radius) +" " +str(elt.direction)+ " " + str(elt.origine.x) + " " +str(elt.origine.y)+ " " + str(elt.velocity))
                f.write("\n")
    return f
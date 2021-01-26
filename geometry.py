class Point:
    def __init__(self, x, y,nbcercle = 0):
        self.x = x
        self.y = y
        self.nbcercle = nbcercle

#L'attribut nbcercle compte le nombre de cercle situé sur ce point.

    def __repr__(self):
        return ("(" + str(self.x) + "," + str(self.y) +")" + " et nb_cercle =" + str(self.nbcercle))
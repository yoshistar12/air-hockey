import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def dot(self, v2):
        'Skalarprodukt av to vektorer, returnerer et talls'
        return self.x*v2.x + self.y*v2.y
    def get_tuple(self):
        'Her går vi fra Vector(x, y) til vanlig (x, y)'
        return self.x, self.y
    def get_int_tuple(self):
        'Her går vi fra Vector(x, y) til (int(x), int(y))'
        return int(self.x), int(self.y)
    def normalize(self):
        'Returnerer en vektor med samme retning men lengde 1'
        mag = self.mag()
        return Vector(self.x / mag, self.y / mag)
    def __mul__(self, v2):
        'To typer av multiplikasjon'
        if isinstance(v2, (int, float)): # hvis et tall og en vektor
            return Vector(self.x * v2, self.y * v2) # skalarmultiplikasjon for et tall og en vektor
        elif isinstance(v2, Vector): # hvis to vektorer
            return self.dot(v2) # skalarprodukt av to vektorer
    def __rmul__(self, v2):
        'Dette gjør at vi kan skrive tall * vektor, ikke bare vektor * tall (gjør skalarmultiplikasjon assosiativ)'
        return self.__mul__(v2)
    def __add__(self, v2):
        'Vanlig vektoraddisjon'
        return Vector(self.x + v2.x, self.y + v2.y)
    def __sub__(self, v2):
        'Vanlig vektorsubtraksjon'
        return Vector(self.x - v2.x, self.y - v2.y)
    def angle(self, v2):
        'Returnerer vinkelen mellom to vektorer'
        return math.acos((self.dot(v2) / (self.mag() * v2.mag())))
    def mag(self):
        'Returnerer lengden av vektoren'
        return math.sqrt(self.x**2 + self.y**2)
    def __str__(self):
        'Dette er får at ting som print(Vector(x, y)) skal funke'
        return f'<{self.x}, {self.y}>'

def angle(v1, v2):
    'Dette er en wrapper for v1.angle(v2), en annen måte å skrive det på'
    return v1.angle(v2)

def dot(v1, v2):
    'Dette er en wrapper for v1.dot(v2), en annen måte å skrive det på'
    return v1.dot(v2)

    


    

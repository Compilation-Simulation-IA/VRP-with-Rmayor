import threading
import time

tiempo_global = 0  # Inicializamos la variable global en 0

class Vehicle(threading.Thread):
    def __init__(self, id, speed, destination):
        super().__init__()  # Inicializamos el hilo padre
        self.id = id
        self.speed = speed
        self.destination = destination

    def __repr__(self) -> str:
        return f"<Vehicle({self.id})>" 
    
    def __str__(self):
        return f"<Vehicle: ID {self.id}>" 
    
    def run(self):
        global tiempo_global  # Declaramos que vamos a usar la variable global
        
        print(f"El vehiculo {self.id} esta comenzando a moverse hacia {self.destination} a una velocidad de {self.speed} km/h")
        distancia_recorrida = 0
        while distancia_recorrida < self.destination:
            # Calculamos la distancia recorrida en esta iteración
            distancia_recorrida += self.speed
            # Actualizamos el tiempo global
            tiempo_global += 1
            # Esperamos 1 segundo antes de continuar con la siguiente iteración
            time.sleep(1)
        
        print(f"El vehiculo {self.id} ha llegado a su destino despues de recorrer una distancia de {distancia_recorrida} km en {tiempo_global} segundos")

# Creamos 3 hilos para 3 vehículos que se mueven a distintas velocidades y destinos
vehiculo1 = Vehicle(1, 50, 100)
vehiculo2 = Vehicle(2, 40, 100)
vehiculo3 = Vehicle(3, 5, 100)

# Iniciamos los hilos
vehiculo1.start()
vehiculo2.start()
vehiculo3.start()

# Esperamos a que todos los hilos terminen
vehiculo1.join()
vehiculo2.join()
vehiculo3.join()

# Una vez que todos los hilos han terminado, podemos mostrar el tiempo total transcurrido
print(f"El tiempo total transcurrido fue de {tiempo_global} segundos")

#Mostrar información final de los vehículos
print(vehiculo1)
print(vehiculo2)
print(vehiculo3)
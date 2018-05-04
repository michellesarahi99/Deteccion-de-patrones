import neurolab as nl
import numpy as np
import scipy as sp

datos = np.matrix(sp.genfromtxt("datos.csv", delimiter=" "))

#datos de entrada a la neurona
entrada = datos[:,:-3]
#datos de salida de la neurona
objetivo = datos[:,-3:]
#max min para cada dato de entrada a la neurona 
maxmin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])

# valores para las capas de la neurona 
capa_entrada = entrada.shape[0]
capa_oculta1 = int(capa_entrada*0.5)
capa_oculta2 = int(capa_entrada*0.33)
capa_salida = 3

# Crear red neuronal con 4 capas 1 de entrada 2 ocultas y 1 de salida 
rna = nl.net.newff(maxmin, [ capa_entrada, capa_entrada, capa_oculta1, capa_salida])

#Cambio de algoritmo a back propagation simple
rna.trainf = nl.train.train_gd

#Datos para la red
error = rna.train(entrada, objetivo, epochs=10000, show=100, goal=0.02, lr=0.01)

# Simulacion RNA
rna.save("red-entrenada.tmt")
salida = rna.sim(entrada)

print (salida)
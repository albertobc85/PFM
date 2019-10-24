import Log as logging

def crea_matriz(m):
    '''
    Esta función crea una matríz vacía con m filas y n columnas.
    m : Número de filas y columnas
    '''
    matriz = []
    for i in range(1,m):
        a = ['O']*m
        matriz.append(a)
    return matriz

def matriz2str(matriz):
    '''
    Esta función recorre los elementos de los vectores de la matriz
    y los separa mediante una expresión regular.
    matriz : Array de m
    '''
    cadena = ''
    for i in range(len(matriz)):
        cadena += ' '
        for j in range(len(matriz[i])):
            cadena += '{:>4s}'.format(str(matriz[i][j]))
        cadena += ' \n'
    return cadena

def line2str(vector):
    '''
    Esta función imprime mediante espacios ({7s}) los elementos
    de un vector.
    vector : 
    '''
    cadena = ''
    for i in range(len(vector)):
        cadena += '{:>7s}'.format(str(vector[i]))
    return cadena

def dibujar_tablero():
    
    
    m = int(input('¿Cuál quieres que sean las dimensiones del tablero ? \n'))
    
    while True:
        if m < 20:
            m = int(input('Lo siento, pero las dimensiones tienen que ser mínimo de 20x20 \n'
                          'Por favor, vuelva a introducir un número: \n'))
        else:
            mat3=crea_matriz(m)
            break
        
    print(matriz2str(mat3))
    sep=['-']*(m-5)
    print(line2str(sep))    
    return mat3

aux=dibujar_tablero()

flota = {'Portaaviones':5,
             'Buque de guerra':4,
             'Submarino':3,
             'Destructor':3,
             'Lancha':2,}

claves_flota = flota.keys()
valor_flota = flota.values()

coordenadas_xy = []

numeros = '1234567890,'

while True:
    for clave in claves_flota:
    
        coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
        
        while not ',' in coordenadas:
            print('Error. No ha introducido la coma "," Vuelva a introducir las coordenadas.')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
            
            if ',' in coordenadas:
                coordenadas = coordenadas.split(',')
                while coordenadas[0] == '' or coordenadas[1] == '':
                    print('Error. No ha introducido todas las coordenadas. Vuelva a introducir las coordenadas.')
                    coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                                    f'del siguiente barco: "{clave}": ')
                    
                break
        coordenadas = coordenadas.split(',')
        
            
        while coordenadas[0] == '' or coordenadas[1] == '':
            print('Error. No ha introducido todas las coordenadas. Vuelva a introducir las coordenadas.')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
            coordenadas = coordenadas.split(',')
            
        while coordenadas in coordenadas_xy:    
            print('Error. Ya hay un barco con estas coordenadas. Vuelva a introducir unas nuevas coordenadas.')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
            coordenadas = coordenadas.split(',')
            
        while int(coordenadas[0]) > len(aux) or int(coordenadas[1]) > len(aux):
            print('Error. La coordenada recibida es más grande que el tablero. Vuelva a introducir unas nuevas coordenadas.')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
            coordenadas = coordenadas.split(',')
            
        while coordenadas[0] == '0' or coordenadas[1] == '0':
            print('Error. No se acepta el número 0 como coordenada. Debe de empezar desde 1.\n'
                 'Vuelva a introducir unas nuevas coordenadas.')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                            f'del siguiente barco: "{clave}": ')
            coordenadas = coordenadas.split(',')
            
        
            
        coordenadas_xy.append(coordenadas)
        
        
    break
        
coordinates_x = [x for x in coordenadas_xy]

def coordenadas_a_entero(coordinates2):

    coordinates = []
    for n in coordinates2:
        n = list(map(int, n))
        coordinates.append(n)
    return coordinates

aux=coordenadas_a_entero(coordenadas_xy)


'''
Al empezar la cuenta del tablero en 0, es necesario
restarle 1 a cada valor de coordenadas de cada barco para
que estén situados en su posición
'''

enteros = []
for n in aux:
    print(n)
    n[0] -= 1
    n[1] -= 1
    print('--------')
    print(n)
    enteros.append(n)

def sustituyendo(mat2, coord):
    try:
        for x in coord:
            inicio = mat2[int(x[1])][int(x[0])]='X'
    except:
        pass
           
    return mat2

def dibujarBarcoIzqda(coordenadas_xy,valor_flota):
    barco = []
    barco.append(coordenadas_xy)
    print(barco)
"""     for x in range(1,valor_flota):
        aux = coordenadas_xy[1] - x
        elemntSeg=[coordenadas_xy[0], aux]
        barco.append(elemntSeg)
    return barco """

def dibujarBarcoDcha(coordenadas_xy,valor_flota):
    barco = []
    barco.append(coordenadas_xy)
    for x in range(1,valor_flota):
        aux = coordenadas_xy[1] +x
        elemntSeg=[coordenadas_xy[0], aux]
        barco.append(elemntSeg)
    print(barco)
    return barco

def dibujarBarcoArriba(inicio,longitud):
    barco = []
    barco.append(inicio)
    for x in range(1,longitud):
        aux = inicio[0] - x
        elementoPrimero = [aux,inicio[1]]
        barco.append(elementoPrimero)
        print(elementoPrimero)
    print(barco)
    return barco

def dibujarBarcoAbajo(inicio,longitud):
    barco = []
    barco.append(inicio)
    for x in range(1,longitud):
        aux = inicio[0] + x
        elementoPrimero = [aux,inicio[1]]
        barco.append(elementoPrimero)
        print(elementoPrimero)
    return barco

def ladoDir():
    for clave in claves_flota:
        lado = input(f'¿Hacia donde quiere dirigir el {clave} ? 4 opciones: Izquierda(I), derecha(D), arriba(A), abajo(B)')
        if lado == 'I' or 'i':
            return dibujarBarcoIzqda(aux[0],5)
        elif lado == 'D' or 'd':
            dibujarBarcoDcha(coordinates_x)
        elif lado == 'A' or 'a':
            dibujarBarcoArriba(coordinates_x)
        elif lado == 'B' or 'b':
            dibujarBarcoAbajo(coordinates_x)
        else :
            print("ERROR no ha introducido I,D,A,B")

#aux=sustituyendo(aux,ladoDir())
#print(matriz2str(aux))
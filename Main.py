'''
Estas son las librerías que van a ser utilizadas en este proyecto.
'''
import sys
import random
import time
import numpy
import tqdm
import colorama
import pygame


def crea_matriz(MATRIX):

    '''
    Esta función crea una matríz vacía con m filas y n columnas.
    MATRIX : Número de filas y columnas.
    '''

    matriz = []
    for i in range(0,MATRIX):
        a = ['O']*MATRIX
        matriz.append(a)
    return matriz

def matriz_a_string(matriz):

    '''
    Esta función recorre los elementos de los vectores de la matriz
    y los separa mediante una expresión regular.
    matriz : Array de MATRIX.
    '''

    cadena = ''
    for i in range(len(matriz)):
        cadena += ' '
        for j in range(len(matriz[i])):
            cadena += '{:>4s}'.format(str(matriz[i][j]))
        cadena += ' \n'
    return cadena

def linea_a_string(vector):

    '''
    Esta función imprime mediante espacios ({7s}) los elementos
    de un vector.
    '''

    cadena = ''
    for i in range(len(vector)):
        cadena += '{:>7s}'.format(str(vector[i]))
    return cadena



def dibujar_tablero():    

    '''
    Esta función dibujará el tablero para el usuario, pedirá las dimensionaes y las coordenadas.
    '''

    global MATRIX
    #Si utilizaba colorama dentro de un input, la salida daba un número tipo ?[34m y no daba color al texto,
    #Por lo que se decide crear un print antes para dar color al texto que venga después de dicho print
    print(colorama.Fore.GREEN + '')
    MATRIX = int(input('¿Cuál quieres que sean las dimensiones del tablero ? \n'))
    
    while True:
        if MATRIX < 20:
            print(colorama.Fore.RED + '')
            MATRIX = int(input('Lo siento, pero las dimensiones tienen que ser mínimo de 20x20 \n'
                          'Por favor, vuelva a introducir un número: \n'))
        else:
            mat3=crea_matriz(MATRIX)
            break
        
  #  sep=['-']*(MATRIX-5)  
    return mat3

def cumple_condiciones(coordenadas):

    '''
    Función que comprueba que no existen nulos, letras ,... entre las coordenas y que se inserta de forma correcta.
    '''

    resultado_no_cumple=True
    if not ',' in coordenadas:
        print(colorama.Fore.RED + '')
        print('ERROR: No ha introducido la coma "," Vuelva a introducir las coordenadas.')
    else:
        coordenadas = coordenadas.split(',')
        global posicion
        posicion = coordenadas
        if coordenadas[0].isdigit() == False or coordenadas[1].isdigit() == False:
            print(colorama.Fore.RED + '')
            print('Los valores introducidos entre las comas no son válidos, Vuelva a introducir las coordenadas.')
        elif int(coordenadas[0]) > MATRIX or int(coordenadas[1]) > MATRIX:
            print(colorama.Fore.RED + '')
            print('Los valores introducidos entre las comas no son válidos, Vuelva a introducir las coordenadas.')
            print(f'Recuerda que las dimensiones máximas son {MATRIX}.')
        else:
            resultado_no_cumple=False
    return resultado_no_cumple, coordenadas

#def musica():

    '''
    Función con la que, mediante el módulo pygame, reproducimos música para hacer más ameno el juego.
    '''
    
    #pygame.mixer.pre_init()
    #pygame.mixer.init()
    #pygame.mixer.music.load('d:\Trabajo Fin de Master\classic-vgm-209-mike-tysons-punch-out-training-theme.wav')
    #pygame.mixer.music.play(-1)

def pedir_coordenadas(tablero):

    '''
    Esta función pedirá las coordenadas al usuario y hará las comprobaciones para ver que ha introducido correctamente
    las coordenadas.
    En caso de no introducirlas bien volverá a preguntar al usuario hasta introducirlas correctamente. En caso de que
    sí se hayan introducido correctamente, la función llevará a la función "pedir_direccion()" para preguntar al usuario
    por la posición del barco (izquierda, derecha, arriba o abajo).
    '''

    flagCondicionNoCumple=True
    flota = {'Portaaviones':5,
                'Buque de guerra':4,
                'Submarino':3,
                'Destructor':3,
                'Lancha':2}

    
    claves_flota = flota.keys()
    global VALOR_FLOTA
    VALOR_FLOTA = flota.values()
   
    coordenadas_xy = []

    for clave in claves_flota: 
        flagCondicionNoCumple=True   
        while flagCondicionNoCumple:
            
            print(colorama.Fore.GREEN + '')
            coordenadas = input(f'Introduce la coordenada "x", y separado por una coma, la coordenada "y" \n'
                                f'del siguiente barco: "{clave}": ')
            
            flagCondicionNoCumple, coordenadas2 =cumple_condiciones(coordenadas)
            #Si las coordenadas tienen el formato correcto pasamos a comprobar si ya han sido utilizadas
            if flagCondicionNoCumple == False:     
                flagCondicionNoCumple=True
                coordenadas2 = list(map(int, coordenadas2))
                if coordenadas2 in coordenadas_xy:
                    print(colorama.Fore.RED + '')
                    print('Error. Ya hay un barco con estas coordenadas. Vuelva a introducir unas nuevas coordenadas.')
                #Si las coordenadas no han sido introducidas anteriormente
                else: 
                    coord=pedir_direccion(coordenadas2,flota.get(clave),clave)
                    coordenadas_xy.extend(coord)
                    flagCondicionNoCumple=True
                    break
              
    colocar_coord_usuario = numpy.array(coordenadas_xy)
    global COORD_USUARIO
    COORD_USUARIO = colocar_coord_usuario - 1
    return COORD_USUARIO

def sustituyendo(mat2, coord):

    '''
    Esta función sustituye en las coordenadas dadas en la posición de la matriz por "X".
    '''
    for x in coord:
        mat2[x[0]][x[1]]='X'
    return mat2

def sustituyendo_partida(TABLERO_MAQUINA, coord):

    '''
    Esta función sustituye en las coordenadas dadas en la posición de la matriz por "X".
    '''     
    TABLERO_MAQUINA[coord[0]][coord[1]]='T'
    return TABLERO_MAQUINA

def dibujar_barco_izquierda(coordenadas_xy,VALOR_FLOTA):

    '''
    Esta función dibuja las coordenadas del barco hacia la izquierda
    '''

    barco = []
    for x in range(1,VALOR_FLOTA):
        aux = coordenadas_xy[1] - x
        elemntSeg=[coordenadas_xy[0], aux]
        barco.append(elemntSeg)
    return barco

def dibujar_barco_derecha(coordenadas_xy,VALOR_FLOTA):

    '''
    Esta función dibuja las coordenadas del barco hacia la derecha.
    '''

    barco = []
    barco.append(coordenadas_xy)
    for x in range(1,VALOR_FLOTA):
        aux = coordenadas_xy[1] +x
        elemntSeg=[coordenadas_xy[0], aux]
        barco.append(elemntSeg)
    return barco

def dibujar_barco_arriba(coordenadas_xy,VALOR_FLOTA):

    '''
    Esta función dibuja las coordenadas del barco hacia la arriba.
    '''

    barco = []
    barco.append(coordenadas_xy)
    for x in range(1,VALOR_FLOTA):
        aux = coordenadas_xy[0] - x
        elementoPrimero = [aux,coordenadas_xy[1]]
        barco.append(elementoPrimero)
    return barco

def dibujar_barco_abajo(coordenadas_xy,VALOR_FLOTA):

    '''
    Esta función dibuja las coordenadas del barco hacia la abajo.
    '''

    barco = []
    barco.append(coordenadas_xy)
    for x in range(1,VALOR_FLOTA):
        aux = coordenadas_xy[0] + x
        elementoPrimero = [aux,coordenadas_xy[1]]
        barco.append(elementoPrimero)
    return barco

def pedir_direccion(coord,longitud,clave):

    '''
    Esta función es llamada en pedir_coordenadas() y pregunta al usuario la dirección en que quiere introducir el barco
    (izquierda, derecha, arriba, abajo).
    Comprueba que hay suficiente espacio para poder introducir el barco hacia ese lado y, en caso positivo, se podrá 
    introducir, y en caso negativo, dará error y volverá a preguntar sobre que lado quiere.
    '''

    resultado_lista_entero =  list(map(int, coord))

    while True:
        print(colorama.Fore.GREEN + '')
        lado = input(f'¿Hacia donde quiere dirigir el {clave} ? 4 opciones: Izquierda(I), derecha(D), arriba(A), abajo(B)')
    
        if lado.lower() == 'i':
            if clave == 'Portaaviones':
                if int(posicion[1]) < 5:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Izquierda. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_izquierda(resultado_lista_entero,longitud)
                    
                    break
            elif clave == 'Buque de guerra':
                if int(posicion[1]) < 4:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Izquierda. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_izquierda(resultado_lista_entero,longitud)
                    break
            elif clave == 'Destructor' or clave == 'Submarino':
                if int(posicion[1]) < 3:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Izquierda. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_izquierda(resultado_lista_entero,longitud)
                    break
            elif clave == 'Lancha':
                if int(posicion[1]) < 2:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Izquierda. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_izquierda(resultado_lista_entero,longitud)
                    break
        
        elif lado.lower() == 'd':
            if clave == 'Portaaviones':
                if int(posicion[1]) > (MATRIX-5):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Derecha. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_derecha(resultado_lista_entero,longitud)
                    break
            elif clave == 'Buque de guerra':
                if int(posicion[1]) > (MATRIX-4):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Derecha. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_derecha(resultado_lista_entero,longitud)
                    break
            elif clave == 'Destructor' or clave == 'Submarino':
                if int(posicion[1]) > (MATRIX-3):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Derecha. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_derecha(resultado_lista_entero,longitud)
                    break
            elif clave == 'Lancha':
                if int(posicion[1]) > (MATRIX-2):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia la Derecha. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_derecha(resultado_lista_entero,longitud)
                    break
        elif lado.lower() == 'a':
            if clave == 'Portaaviones':
                if int(posicion[0]) < 5:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Arriba. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_arriba(resultado_lista_entero,longitud)
                    break
            elif clave == 'Buque de guerra':
                if int(posicion[0]) < 4:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Arriba. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_arriba(resultado_lista_entero,longitud)
                    break
            elif clave == 'Destructor' or clave == 'Submarino':
                if int(posicion[0]) < 3:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Arriba. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_arriba(resultado_lista_entero,longitud)
                    break
            elif clave == 'Lancha':
                if int(posicion[0]) < 2:
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Arriba. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_arriba(resultado_lista_entero,longitud)
                    break
        
        elif lado.lower() == 'b':
            if clave == 'Portaaviones':
                if int(posicion[0]) > (MATRIX-5):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Abajo. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_abajo(resultado_lista_entero,longitud)
                    break
            elif clave == 'Buque de guerra':
                if int(posicion[0]) > (MATRIX-4):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Abajo. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_abajo(resultado_lista_entero,longitud)
                    break
            elif clave == 'Destructor' or clave == 'Submarino':
                if int(posicion[0]) > (MATRIX-3):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Abajo. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_abajo(resultado_lista_entero,longitud)
                    break
            elif clave == 'Lancha':
                if int(posicion[0]) > (MATRIX-2):
                    print(colorama.Fore.RED + '')
                    print(f'No puede elegir poner el barco {clave} hacia Abajo. Por favor, inténtelo de nuevo.')
                else:
                    res = dibujar_barco_abajo(resultado_lista_entero,longitud)
                    break 
        else :
            print(colorama.Fore.RED + '')
            print("ERROR no ha introducido I,D,A,B")
    return res



def crea_matriz_maquina():

    '''
    Esta función crea automáticamente un tablero para la máquina del mismo tamaño que el elegido por el usuario.
    '''

    global MATRIZ_MAQUINA
    MATRIZ_MAQUINA = crea_matriz(MATRIX)
    return MATRIZ_MAQUINA
    

def lista_aleatorios():

    '''
    En esta función conseguimos coordenadas para la máquina de forma aleatoria.
    '''

    coordenadas_aleatorias = []
    coordenada_x = random.randint(0,MATRIX-1)
    coordenada_y = random.randint(0,MATRIX-1)
    coordenadas_aleatorias.append([coordenada_x,coordenada_y])
    return coordenadas_aleatorias

def posicion_barcos_maquina(tablero):

    '''
    En esta función, se coloca la posición de los barcos de la máquina de forma aleatoria (siempre y cuando cumplan
    con los requisitos de espacio).
    '''
    
    letras = ['i','d','a','b']
    i = 0
    coordenadas = []

    for clave in VALOR_FLOTA:
        numeros_aleatorios = lista_aleatorios()
        resultado_lista_entero =  list(map(int, numeros_aleatorios[i]))
        posicion = random.choice(letras)

        if clave == 5:

            if resultado_lista_entero[1] < 5 and resultado_lista_entero[0] < 5:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 5) and resultado_lista_entero[0] > (MATRIX - 5):
                letras = ['i','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 5) and resultado_lista_entero[1] < 5:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 5 and resultado_lista_entero[1] > (MATRIX - 5):
                letras = ['i','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 5):
                letras = ['i','d','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif letras == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] < 5:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 5:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 5):
                letras = ['i','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            else:
                letras = ['i','d','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])
                    

        if clave == 4:
            if resultado_lista_entero[1] < 4 and resultado_lista_entero[0] < 4:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 4) and resultado_lista_entero[0] > (MATRIX - 4):
                letras = ['i','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 4) and resultado_lista_entero[1] < 4:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 4 and resultado_lista_entero[1] > (MATRIX - 4):
                letras = ['i','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 4):
                letras = ['i','d','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] < 4:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 4:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 4):
                letras = ['i','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            else:
                letras = ['i','d','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])
                    

        if clave == 3:
            if resultado_lista_entero[1] < 3 and resultado_lista_entero[0] < 3:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 3) and resultado_lista_entero[0] > (MATRIX - 3):
                letras = ['i','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 3) and resultado_lista_entero[1] < 3:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 3 and resultado_lista_entero[1] > (MATRIX - 3):
                letras = ['i','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 3):
                letras = ['i','d','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] < 3:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 3:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 3):
                letras = ['i','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            else:
                letras = ['i','d','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])
                    

        if clave == 2:
            if resultado_lista_entero[1] < 2 and resultado_lista_entero[0] < 2:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 2) and resultado_lista_entero[0] > (MATRIX - 2):
                letras = ['i','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 2) and resultado_lista_entero[1] < 2:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 2 and resultado_lista_entero[1] > (MATRIX - 2):
                letras = ['i','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] > (MATRIX - 2):
                letras = ['i','d','a']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] < 2:
                letras = ['d','a']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[0] < 2:
                letras = ['d','b']
                posicion = random.choice(letras)
                if posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            elif resultado_lista_entero[1] > (MATRIX - 2):
                letras = ['i','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

            else:
                letras = ['i','d','a','b']
                posicion = random.choice(letras)
                if posicion == 'i':
                    resultado = dibujar_barco_izquierda(resultado_lista_entero,clave)
                elif posicion == 'd':
                    resultado = dibujar_barco_derecha(resultado_lista_entero,clave)
                elif posicion == 'a':
                    resultado = dibujar_barco_arriba(resultado_lista_entero,clave)
                else:
                    resultado = dibujar_barco_abajo(resultado_lista_entero,clave)
                for coordenada in range(len(resultado)):
                    numeros_aleatorios.append(resultado[coordenada])

        coordenadas.append(numeros_aleatorios)
        
    lista_coordenadas = [item for sublist in coordenadas for item in sublist ]
    global COORD_MAQUINA
    colocar_coord_maquina = numpy.array(lista_coordenadas)
    COORD_MAQUINA = colocar_coord_maquina - 0
    
    
    return COORD_MAQUINA


def barra_progreso():

    '''
    Función para crear una barra de progreso.
    '''
    print(colorama.Fore.BLUE + '')
    print('Por favor, espera mientras se crea el tablero de la máquina... tic, tac, tic, tac...')
    for i in tqdm.tqdm(range(1000)):
        time.sleep(0.01)

    print(colorama.Fore.YELLOW + '')
    print('Proceso completado.')
    time.sleep(random.randint(1, 4))

def espera():

    '''
    Función para ralentizar la pantalla para que el juego pueda ser leído mas detenidamente.
    '''

    time.sleep(2)

def cumple_condiciones_partida(NUM_USUARIO):

    '''
    Función que comprueba que no existen nulos, letras ,... entre las coordenas y que se inserta de forma correcta
    '''

    resultado_no_cumple=True
    if not ',' in NUM_USUARIO:
        print(colorama.Fore.RED + '')
        print('ERROR: No ha introducido la coma "," Vuelva a introducir las coordenadas.')
    else:
        NUM_USUARIO = NUM_USUARIO.split(',')
        if NUM_USUARIO[0].isdigit() == False or NUM_USUARIO[1].isdigit() == False:
            print(colorama.Fore.RED + '')
            print('Los valores introducidos entre las comas no son válidos, Vuelva a introducir las coordenadas.')
        else:
            resultado_no_cumple=False
    return resultado_no_cumple

def cumple_condiciones_maquina(coordenadas):

    '''
    Función que comprueba que no existen nulos, letras ,... entre las coordenas y que se inserta de forma correcta.
    '''

    resultado_no_cumple=False
    coordenadas = coordenadas
    return resultado_no_cumple, coordenadas


CONTADOR_MAQUINA = 0

def contador():

    '''
    Función para incrementar el contador de la máquina.
    '''

    global CONTADOR_MAQUINA
    CONTADOR_MAQUINA += 1



def chequeo_maquina(lista_num,lista_usuario_m):

    '''
    En esta función, la máquina, de manera aleatoria, chequea en el tablero del usuario buscando los barcos 
    del usuario para hundirlos. Si da a alguno, saldrá "tocado", si no da a nada, saldrá "agua"
    '''
    
    i = 0
    tiempo_maquina = False
    coord_aleatorias = []
    coord_totales_maq = []
    chequeo_len = []
    coordenadas_x_maquina = random.randint(0,MATRIX -1)
    coordenadas_y_maquina = random.randint(0,MATRIX -1)
    coord_aleatorias.append([coordenadas_x_maquina,coordenadas_y_maquina])

    chequear_condicion = True
    while chequear_condicion:
        chequear_condicion,coor =cumple_condiciones_maquina(coord_aleatorias)
        if chequear_condicion == False:     
            chequear_condicion=True
            if coord_aleatorias in coord_totales_maq or coord_aleatorias in chequeo_len:
                break
            else:
                lista_num.append(coord_aleatorias)
                coord_aleatorias = list(map(int, coord_aleatorias[i]))
                coord_aleatorias = numpy.array(coord_aleatorias)
                coord_totales_maq.append(coord_aleatorias)
                print(colorama.Fore.GREEN + '') 
                coord_imp=[coord_aleatorias[0]+1,coord_aleatorias[1]+1]
                print(f'La máquina decide disparar en las coodenadas... {coord_imp }')
                espera()
                global matriz_usuario2
                for n in range(len(COORD_USUARIO)):
                    array_COORD_USUARIO = COORD_USUARIO[n]
                    if numpy.array_equal(coord_aleatorias,array_COORD_USUARIO):
                        print(colorama.Fore.RED + '')
                        print('¡¡Tocado!!')
                        chequeo_len.append(coord_aleatorias)
                        espera()
                        contador()
                        posicion=coord_aleatorias
                        matriz_usuario2=sustituyendo_partida(matriz_usuario, posicion)
                        print(colorama.Fore.WHITE + '')
                        print(matriz_a_string(matriz_usuario2))
                        chequear_condicion = False
                        
                        break
                    elif not numpy.array_equal(coord_aleatorias,array_COORD_USUARIO): 
                        if n == len(COORD_USUARIO)-1 :
                            print(colorama.Fore.GREEN + '') 
                            print('Agua')
                            espera()
                            contador()
                            posicion=coord_aleatorias
                            matriz_usuario2=sustituyendo_partida(matriz_usuario, posicion)
                            print(colorama.Fore.WHITE + '')
                            print(matriz_a_string(matriz_usuario2))
                            chequear_condicion = False
                            break
        


    if len(chequeo_len) == len(COORD_USUARIO):
        final_partida()

    elif CONTADOR_MAQUINA == (MATRIX + 10):
        final_partida()

    tiempo_maquina = True
    if tiempo_maquina == True:
        chequeo_usuario(lista_num,lista_usuario_m)

chequeo_barcos = []

def chequeo_usuario(lista_maq,lista_usuario):

    '''
    En esta función, el usuario elige unas coordenadas que chequean en el tablero de la máquina buscando 
    los barcos del usuario para hundirlos. Si da a alguno, saldrá "tocado", si no da a nada, saldrá "agua"
    '''
    global NUM_USUARIO
    tiempo_usuario = True
    contador = 0
    #lista_usuario = []
    chequear_condicion = True
    while chequear_condicion:
        print(colorama.Fore.GREEN + '')
        NUM_USUARIO= input('Introduce la coordenada "x", y separado por una coma, la coordenada "y"')
        chequear_condicion,coor =cumple_condiciones(NUM_USUARIO)
        #print(type(NUM_USUARIO))
        if chequear_condicion == False:     
            chequear_condicion=True
            if NUM_USUARIO in lista_usuario:
                print(colorama.Fore.RED + '')
                print('Error. Ya habías introducido estas coordenadas anteriormente. Vuelva a introducir unas nuevas coordenadas.')
            #Si las coordenadas no han sido introducidas anteriormente
            else:
                lista_usuario.append(NUM_USUARIO)
                NUM_USUARIO = NUM_USUARIO.split(',')
                NUM_USUARIO = list(map(int, NUM_USUARIO))
                chequeo = numpy.array(NUM_USUARIO)
                chequeo = chequeo - 1
                for n in range(len(COORD_MAQUINA)):
                    array_COORD_MAQUINA = COORD_MAQUINA[n]
                    tiempo_usuario = False
                    if numpy.array_equal(chequeo,array_COORD_MAQUINA):
                        chequeo_barcos.append(chequeo)
                        print(colorama.Fore.MAGENTA + '')
                        print('¡¡Tocado!!')
                        espera()
                        contador += 1
                        print(colorama.Fore.GREEN + '')
                        print('Turno para la máquina, suerte...')
                        espera()
                        posicion=chequeo
                        global TABLERO_MAQUINA2
                        TABLERO_MAQUINA2=sustituyendo_partida(TABLERO_MAQUINA, posicion)
                        chequear_condicion = False
                        break
                    elif not numpy.array_equal(chequeo,array_COORD_MAQUINA): 
                        if n == len(COORD_MAQUINA)-1 :  
                            print(colorama.Fore.CYAN + '')
                            print('Agua')
                            espera()
                            contador += 1
                            print(colorama.Fore.GREEN + '')
                            print('Turno para la máquina, suerte...')
                            espera()
                            posicion=chequeo
                            TABLERO_MAQUINA2=sustituyendo_partida(TABLERO_MAQUINA, posicion)
                            chequear_condicion = False
                            break


    if len(chequeo_barcos) == len(COORD_MAQUINA-4):
        final_partida()
    elif contador == (MATRIX + 10):
            final_partida()
    
    if tiempo_usuario == False:
        chequeo_maquina(lista_maq,lista_usuario)


def final_partida():

    '''
    Esta función muestra el resultado de la partida, mostrando los tableros y preguntado para empezar una nueva
    partida.
    '''

    print(colorama.Fore.MAGENTA + '')
    print('La partida ha terminado. A continuación se muestran los tableros del usuario y de la máquina.')
    espera()
    espera()
    print('')
    print(colorama.Fore.GREEN + '')
    print('El tablero de la máquina ha quedado del siguiente modo:')
    espera()
    print(colorama.Fore.WHITE + '')
    print(matriz_a_string(TABLERO_MAQUINA2))
    print('')
    print(colorama.Fore.GREEN + '')
    print('El tablero del usuario ha quedado del siguiente modo:')
    espera()
    print(colorama.Fore.WHITE + '')
    print(matriz_a_string(matriz_usuario2))
    print(colorama.Fore.RED + '')
    empezar_de_nuevo = input('¿Quieres volver a jugar? Y/N ')  
    empezar_de_nuevo = empezar_de_nuevo.upper()
    if empezar_de_nuevo ==  'Y':
        main()
    else:
        sys.exit(0) 
            
    

def main():

    '''
    Función que va llamando a las diferentes funciones para realizar el programa.
    '''

    #musica()
    matriz_inicial_usuario=dibujar_tablero()
    posicion_coordenadas_usuario=pedir_coordenadas(matriz_inicial_usuario)
    global matriz_usuario
    matriz_usuario=sustituyendo(matriz_inicial_usuario, posicion_coordenadas_usuario)
    print(colorama.Fore.WHITE + '')
    print(matriz_a_string(matriz_usuario))
    barra_progreso()
    matriz_inicial_maquina=crea_matriz_maquina()
    posicion_coordenadas_maquina=posicion_barcos_maquina(matriz_inicial_maquina)
    global TABLERO_MAQUINA
    TABLERO_MAQUINA=sustituyendo(matriz_inicial_maquina, posicion_coordenadas_maquina)
    lista_maq=[] 
    lista_usu=[]
    chequeo_usuario(lista_maq,lista_usu)



if __name__ == "__main__":
    main()
    

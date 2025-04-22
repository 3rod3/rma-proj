# Make sure to have the server side running in CoppeliaSim:
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

# MHZ: O sim é sempre definido, já quue é um arquivo na mesma pasta do projeto.
import sim
import time

# ================================
# Os import abaixo não estão sendo usados neste arquivo. A minha dúvida é:
# Para que eles seriam usados? O math e o matplot indicam algo com gráficos,
# mas não faço ideia do pra que importar o random, também.
#
# import math
# import random
# import matplotlib
# ================================

print('Program started')
# Just in case, close all opened connections
sim.simxFinish(-1)
# Connect to CoppeliaSim
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
if clientID != -1:
    print('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID,
                                'Funcionando...',
                                sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # variáveis e handle para o robo e o objetivo
    robotname = 'Pioneer_P3DX'
    returnCode, robotHandle = sim.simxGetObjectHandle(clientID,
                                                      robotname,
                                                      sim.simx_opmode_oneshot_wait)
    print('Handle return code:', (returnCode, robotHandle))

    # Handle para as juntas das RODAS
    returnCode, l_wheel = sim.simxGetObjectHandle(clientID,
                                                  '_leftMotor1',
                                                  sim.simx_opmode_oneshot_wait)
    print('Handle return code:', (returnCode, l_wheel))

    returnCode, r_wheel = sim.simxGetObjectHandle(clientID,
                                                  '_rightMotor1',
                                                  sim.simx_opmode_oneshot_wait)
    print('Handle return code:', (returnCode, r_wheel))

    # mostrar os dados da posição e orientação
    [
        returncode,
        [px1, py1, pz1]
    ] = sim.simxGetObjectPosition(clientID,
                                  robotHandle,
                                  -1,
                                  sim.simx_opmode_oneshot_wait)
    print('Robot Pos: ', px1, py1, pz1)
    print('robot pos return code:', returnCode)

    [
        returncode,
        [palpha, pbeta, pgamma]
    ] = sim.simxGetObjectOrientation(clientID,
                                     robotHandle,
                                     -1,
                                     sim.simx_opmode_oneshot_wait)
    print('robot orient: ', palpha, pbeta)
    print('robot orient return code:', returncode)

    # print de coordenadas
    print('as coordenadas da origem são: ', px1, py1)
    print('as orientações do robot: ', palpha, pbeta, pgamma)
    time.sleep(2)
    print(returncode)

    # Lembrar de habilitar o 'Real-time mode'
    t = 0
    startTime = time.time()
    lastTime = startTime

    # mapa do problema
    # MHZ: aqui tá dando problema também. Aparentemente, não tá lendo como
    # uma matriz, e sim como um set
    map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
           [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    campo_pot = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # ======================================================================
    # MHZ: Este loop está UM CRIME. E incompleto. Essa é a última versão? Pois
    # não parece. E tb: O que o loop faz, exatamente?
    for i in range(8, 0):
        for j in range(8, 0):
            somax = 8
            somay = 8
            passo = 0
            inimap = map[somax][somay]
            endmap = map[i][j]

            if endmap == 1:
                campo_pot[i][j] = 99
                continue
            else:
                while somax != i and somay != j:
                    if map[somax - 1][somay] != 1:
                        somax = somax + 1
                        passo = passo + 1
                        continue

                    elif map[somax][somay-1] != 1:
                        somay = somay + 1
                        passo = passo + 1
                        continue

                    #elif
    # ======================================================================

        now = time.time()
        dt = now - lastTime
        t = t + dt
        lastTime = now
        print("tempo =", t, "\r")

    # Parando o robo
    sim.simxSetJointTargetVelocity(clientID,
                                   r_wheel,
                                   0,
                                   sim.simx_opmode_oneshot_wait)
    sim.simxSetJointTargetVelocity(clientID,
                                   l_wheel,
                                   0,
                                   sim.simx_opmode_oneshot_wait)
    print('estou parando: 3 ')

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(
        clientID, 'goodbye CoppeliaSim!', sim.simx_opmode_oneshot)
    print('goodbye Coppeliasim!')

    # Parando a simulação
    sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)
    print('parando a simulação')

    # Before closing the connection to CoppeliaSim, make sure that the last
    # command sent out had time to arrive. You can guarantee this with:
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print('Failed connecting to remote API server')
print('Program ended')

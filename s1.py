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


# =======================================================================
# MHZ: Antes o código tinha um try-except pra fazer load do sim. Como sim é um
# arquivo no mesmo diretório, tirei o try-except. Antes tinha a mensagem abaixo
# em casos de falha ao carregar o arquivo sim.

# print('--------------------------------------------------------------')
# print('"sim.py" could not be imported. This means very probably that')
# print('either "sim.py" or the remoteApi library could not be found.')
# print('Make sure both are in the same folder as this file,')
# print('or appropriately adjust the file "sim.py"')
# print('--------------------------------------------------------------')
# print('')
# =======================================================================

import sim
import time
import math

# ===================
# MHZ: Os import abaixo não são usados, mas estavam aqui antes.
# import random
# import matplotlib
# ===================

#Henri: criei uma função para ler e salvar informações dos sensores que são lidos varias vezes

def lersensor(clientID,sensor):
  [
    returnCode,
    detectionState,
    [detectpx, detectpy, detectpz],
    detectedObjectHandle,
    detectedSurfaceNormalVector
  ] = sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_oneshot_wait)

  print("return code = ", returncode,
        "dectetionstate = ", detectionState,
        "detectedPoint = ", [detectpx, detectpy, detectpz],
        "detectedObjectHandle = ", detectedObjectHandle,
        "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

  detectpx = float("%0.2f" % (detectpx))
  detectpy = float("%0.2f" % (detectpy))
  detectpz = float("%0.2f" % (detectpz))
  return detectionState, detectpx, detectpy, detectpz

print('Program started')
sim.simxFinish(-1)  # just in case, close all opened connections
# Connect to CoppeliaSim
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
if clientID != -1:
    print('Connected to remote API server')
    sim.simxAddStatusbarMessage(
        clientID, 'Funcionando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    # variáveis e handle para o robo e o objetivo
    robotname = 'Pioneer_P3DX'
    returnCode, robotHandle = sim.simxGetObjectHandle(
        clientID, robotname, sim.simx_opmode_oneshot_wait)
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

    print("tempo do momento:")
    while px1 != 4 and py1 != -4:
        # código de tempo
        now = time.time()
        dt = now - lastTime

        t = t + dt
        lastTime = now
        # Velocidade básica (linear)
        v = 0.2
        v1 = 0.5

        # handle de sensores e reitura sensores
        returnCode, l_sensor = sim.simxGetObjectHandle(clientID,
                                                       'sensor0',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, l_sensor))

        returnCode, r_sensor = sim.simxGetObjectHandle(clientID,
                                                       'sensor1',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, r_sensor))

        returnCode, f_sensor = sim.simxGetObjectHandle(clientID,
                                                       'sensor2',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, f_sensor))

        detectionStateL, detectpx0, detectpy0, detectpz0 = lersensor(clientID,l_sensor)
        
        detectionStateR, detectpx1, detectpy1, detectpz1 = lersensor(clientID,r_sensor)

        detectionStateF, detectpx2, detectpy2, detectpz2 = lersensor(clientID,f_sensor)

        [
            returncode,
            [px1, py1, pz1]
        ] = sim.simxGetObjectPosition(clientID,
                                      robotHandle,
                                      -1,
                                      sim.simx_opmode_oneshot_wait)
        if not detectionStateF or detectpz2 > 0.7:
            sim.simxSetJointTargetVelocity(clientID,
                                        r_wheel,
                                        v1,
                                        sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                        l_wheel,
                                        v1,
                                        sim.simx_opmode_oneshot_wait)
            print('estou andando reto')
        time.sleep(0.1)
        
        if detectionStateF and detectpz2 < 0.7:

            while detectionStateF and (detectionStateL == True and detectpz0 <= 0.55) and (detectionStateR == True and detectpz1 <= 0.55):

                print("modo 1: lateral igual, andando reto")
                [
                    returncode,
                    [px1, py1, pz1]
                ] = sim.simxGetObjectPosition(clientID,
                                              robotHandle,
                                              -1,
                                              sim.simx_opmode_oneshot_wait)
                

                detectionStateL, detectpx0, detectpy0, detectpz0 = lersensor(clientID,l_sensor)
        
                detectionStateR, detectpx1, detectpy1, detectpz1 = lersensor(clientID,r_sensor)

                detectionStateF, detectpx2, detectpy2, detectpz2 = lersensor(clientID,f_sensor)


                sim.simxSetJointTargetVelocity(clientID,
                                               r_wheel,
                                               v1,
                                               sim.simx_opmode_oneshot_wait)
                sim.simxSetJointTargetVelocity(clientID,
                                               l_wheel,
                                               -v1,
                                               sim.simx_opmode_oneshot_wait)
                print('estou só o pião da casa própria')

                now = time.time()
                dt = now - lastTime
                t = t + dt
                lastTime = now
                print("tempo =", t, "\r")

            while (detectionStateL == True and detectpz0 > 0.55) or (detectionStateR == True and detectpz1 > 0.55):

                # print("modo 2: lateral diferente, andando reto e corrigindo lateral")

                # detectionStateL, detectpx0, detectpy0, detectpz0 = lersensor(clientID,l_sensor)        
                # detectionStateR, detectpx1, detectpy1, detectpz1 = lersensor(clientID,r_sensor)
                # detectionStateF, detectpx2, detectpy2, detectpz2 = lersensor(clientID,f_sensor)


                # now = time.time()
                # dt = now - lastTime
                # t = t + dt
                # lastTime = now
                # print("tempo =", t, "\r")
                # if detectpz0 > 0.55:
                #     while abs(ang_ori) >= 2:

                #         print("modo 2.1: corrigindo lateral esquerdo")
                #         [
                #             returncode,
                #             [px1, py1, pz1]
                #         ] = sim.simxGetObjectPosition(clientID,
                #                                       robotHandle,
                #                                       -1, sim.simx_opmode_oneshot_wait)

                #         [
                #             returncode,
                #             [palpha, pbeta, pgamma]
                #         ] = sim.simxGetObjectOrientation(clientID,
                #                                          robotHandle,
                #                                          -1,
                #                                          sim.simx_opmode_oneshot_wait)

                #         # MHZ: Linter avisa que rad_ori pode ser unbound.
                #         if pgamma > 0:
                #             ang_ori = ((pgamma*180)/math.pi)
                #         elif pgamma < 0:
                #             ang_ori = -1*(-1*((pgamma*180)/math.pi)-180)+180

                #         ang_ori = float("%0.2f" %(ang_ori))
                #         print('ang orient = ', ang_ori)
                        
                #         kp = 1
                #         v2 = 0.2

                #         sim.simxSetJointTargetVelocity(clientID,
                #                                        r_wheel,
                #                                        v1+(kp*v2),
                #                                        sim.simx_opmode_oneshot_wait)
                #         sim.simxSetJointTargetVelocity(clientID,
                #                                        l_wheel,
                #                                        v1-(kp*v2),
                #                                        sim.simx_opmode_oneshot_wait)
                #         print('ang orient = ', ang_ori)
                #         print('estou girando parcialmente')

                #         detectionStateL, detectpx0, detectpy0, detectpz0 = lersensor(clientID,l_sensor)
        
                #         detectionStateR, detectpx1, detectpy1, detectpz1 = lersensor(clientID,r_sensor)

                #         detectionStateF, detectpx2, detectpy2, detectpz2 = lersensor(clientID,f_sensor)


                #         if (detectionStateL == False or detectionStateR == False) or (detectpz0 <= 0.55 and detectpz1 <= 0.55) or detectpz2 < 0.5:
                #             break
                #         time.sleep(0.5)

                if detectpz1 > 0.55:

                    while abs(ang_ori) >= 2:

                        print("modo 2.2: corrigindo lateral direito")
                        [
                            returncode,
                            [px1, py1, pz1]
                        ] = sim.simxGetObjectPosition(clientID,
                                                      robotHandle,
                                                      -1,
                                                      sim.simx_opmode_oneshot_wait)
                        [
                            returncode,
                            [palpha, pbeta, pgamma]
                        ] = sim.simxGetObjectOrientation(clientID,
                                                         robotHandle,
                                                         -1,
                                                         sim.simx_opmode_oneshot_wait)
                        if pgamma > 0:
                            ang_ori = ((pgamma*180)/math.pi)
                        elif pgamma < 0:
                            ang_ori = -1*(-1*((pgamma*180)/math.pi)-180)+180

                        ang_ori = float("%0.2f" %(ang_ori))
                        print('ang orient = ', ang_ori)

                        kp = 1
                        v2 = 0.2

                        sim.simxSetJointTargetVelocity(clientID,
                                                       r_wheel,
                                                       v1-(kp*v2),
                                                       sim.simx_opmode_oneshot_wait)
                        sim.simxSetJointTargetVelocity(clientID,
                                                       l_wheel,
                                                       v1+(kp*v2),
                                                       sim.simx_opmode_oneshot_wait)

                        print('ang orient = ', ang_ori)
                        print('estou girando parcialmente')

                        detectionStateL, detectpx0, detectpy0, detectpz0 = lersensor(clientID,l_sensor)
        
                        detectionStateR, detectpx1, detectpy1, detectpz1 = lersensor(clientID,r_sensor)

                        detectionStateF, detectpx2, detectpy2, detectpz2 = lersensor(clientID,f_sensor)


                        if (detectionStateL == False or detectionStateR == False) or (detectpz0 <= 0.55 and detectpz1 <= 0.55) or detectpz2 < 0.5:
                            break
                        time.sleep(0.5)

        if (detectionStateF == True and detectpz2 < 0.7):

            sim.simxSetJointTargetVelocity(clientID,
                                           r_wheel,
                                           0,
                                           sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           l_wheel,
                                           0,
                                           sim.simx_opmode_oneshot_wait)
            print('estou parando por condições possíveis')
            print("modo 3: objeto frontal detectado, mudar direção")

            if detectionStateL == True and detectionStateR == True:

                ang_ori = 0
                while abs(ang_ori - 180) > 3:

                    print("modo 3.1: virar 180 graus!")

                    [
                        returncode,
                        [px1, py1, pz1]
                    ] = sim.simxGetObjectPosition(clientID,
                                                  robotHandle,
                                                  -1,
                                                  sim.simx_opmode_oneshot_wait)
                    [
                        returncode,
                        [palpha, pbeta, pgamma]
                    ] = sim.simxGetObjectOrientation(clientID,
                                                     robotHandle,
                                                     -1,
                                                     sim.simx_opmode_oneshot_wait)

                    if pgamma > 0:
                            ang_ori = ((pgamma*180)/math.pi)
                    elif pgamma < 0:
                            ang_ori = -1*(-1*((pgamma*180)/math.pi)-180)+180

                    ang_ori = float("%0.2f" %(ang_ori))
                    print('ang orient = ', ang_ori)


                    sim.simxSetJointTargetVelocity(clientID,
                                                   r_wheel,
                                                   v,
                                                   sim.simx_opmode_oneshot_wait)
                    sim.simxSetJointTargetVelocity(clientID,
                                                   l_wheel,
                                                   -v,
                                                   sim.simx_opmode_oneshot_wait)
                    print('ang orient = ', ang_ori)
                    print('estou girando = 180 graus')

                    dif = 180 - ang_ori
                    print('diferenca = ', dif)
            [
                returncode,
                [px1, py1, pz1]
            ] = sim.simxGetObjectPosition(clientID,
                                          robotHandle,
                                          -1,
                                          sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           r_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           l_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            time.sleep(0.1)

            if detectionStateL == False:
                ang_ori=0
                [
                    returncode,
                    [palpha, pbeta, pgamma]
                ] = sim.simxGetObjectOrientation(clientID,
                                                     robotHandle,
                                                     -1,
                                                     sim.simx_opmode_oneshot_wait)
                ang_inicial=-1*(-1*((pgamma*180)/math.pi)-180)+180
                print(ang_inicial)

                while abs(ang_ori - (ang_inicial+90)) > 3:
                    print("modo 3.2: virar 90 graus! virando para esquerda!")
                    [
                        returncode,
                        [px1, py1, pz1]
                    ] = sim.simxGetObjectPosition(clientID,
                                                  robotHandle,
                                                  -1,
                                                  sim.simx_opmode_oneshot_wait)
                    [
                        returncode,
                        [palpha, pbeta, pgamma]
                    ] = sim.simxGetObjectOrientation(clientID,
                                                     robotHandle,
                                                     -1,
                                                     sim.simx_opmode_oneshot_wait)

                    if pgamma > 0:
                            ang_ori = ((pgamma*180)/math.pi)
                    elif pgamma < 0:
                           ang_ori = -1*(-1*((pgamma*180)/math.pi)-180)+180

                    ang_ori = float("%0.2f" %(ang_ori))
                    print('ang orient = ', ang_ori)

                    sim.simxSetJointTargetVelocity(clientID,
                                                   r_wheel,
                                                   v,
                                                   sim.simx_opmode_oneshot_wait)
                    sim.simxSetJointTargetVelocity(clientID,
                                                   l_wheel,
                                                   -v,
                                                   sim.simx_opmode_oneshot_wait)

                    print('ang orient = ', ang_ori)
                    print('estou girando = 90 graus')

                    dif = 90 - ang_ori
                    print('diferenca = ', dif)

            [
                returncode,
                [px1, py1, pz1]
            ] = sim.simxGetObjectPosition(clientID,
                                          robotHandle,
                                          -1,
                                          sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           r_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           l_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            time.sleep(0.5)

            if detectionStateR == False and detectionStateF == True:
                ang_ori=0 
                while abs(ang_ori - 270) > 3:
                    print("modo 3.1: virar 270 graus! virando para direita!")

                    [
                        returncode,
                        [px1, py1, pz1]
                    ] = sim.simxGetObjectPosition(clientID,
                                                  robotHandle,
                                                  -1,
                                                  sim.simx_opmode_oneshot_wait)
                    [
                        returncode,
                        [palpha, pbeta, pgamma]
                    ] = sim.simxGetObjectOrientation(clientID,
                                                     robotHandle,
                                                     -1,
                                                     sim.simx_opmode_oneshot_wait)

                    if pgamma > 0:
                            ang_ori = ((pgamma*180)/math.pi)
                    elif pgamma < 0:
                            ang_ori = -1*(-1*((pgamma*180)/math.pi)-180)+180

                    ang_ori = float("%0.2f" %(ang_ori))
                    print('ang orient = ', ang_ori)

                    sim.simxSetJointTargetVelocity(clientID,
                                                   r_wheel,
                                                   -v,
                                                   sim.simx_opmode_oneshot_wait)
                    sim.simxSetJointTargetVelocity(clientID,
                                                   l_wheel,
                                                   v,
                                                   sim.simx_opmode_oneshot_wait)
                    print('ang orient = ', ang_ori)
                    print('estou girando = -90 graus')

                    dif = 90 - ang_ori
                    print('diferenca = ', dif)

            [
                returncode,
                [px1, py1, pz1]
            ] = sim.simxGetObjectPosition(clientID,
                                          robotHandle,
                                          -1,
                                          sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           r_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID,
                                           l_wheel,
                                           v1,
                                           sim.simx_opmode_oneshot_wait)
            time.sleep(0.5)

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
    # command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print('Failed connecting to remote API server')
print('Program ended')

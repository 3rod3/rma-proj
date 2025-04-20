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
                                                  '_leftMotor',
                                                  sim.simx_opmode_oneshot_wait)
    print('Handle return code:', (returnCode, l_wheel))

    returnCode, r_wheel = sim.simxGetObjectHandle(clientID,
                                                  '_rightMotor',
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
    while px1 != 2 and py1 != -2:
        # código de tempo
        now = time.time()
        dt = now - lastTime

        t = t + dt
        lastTime = now
        # Velocidade básica (linear)
        v = 0.2
        v1 = 1

        # handle de sensores e reitura sensores
        returnCode, l_sensor = sim.simxGetObjectHandle(clientID,
                                                       'psensor0',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, l_sensor))

        returnCode, r_sensor = sim.simxGetObjectHandle(clientID,
                                                       'psensor1',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, r_sensor))

        returnCode, f_sensor = sim.simxGetObjectHandle(clientID,
                                                       'psensor2',
                                                       sim.simx_opmode_oneshot_wait)
        print('Handle return code:', (returnCode, f_sensor))

        [
            returnCode,
            detectionState0,
            [detectpx0, detectpy0, detectpz0],
            detectedObjectHandle,
            detectedSurfaceNormalVector
        ] = sim.simxReadProximitySensor(clientID,
                                        l_sensor,
                                        sim.simx_opmode_oneshot_wait)

        detectpx0 = float("%0.2f" % (detectpx0))
        detectpy0 = float("%0.2f" % (detectpy0))
        detectpz0 = float("%0.2f" % (detectpz0))

        print("return code = ", returncode,
              "dectetionstate = ", detectionState0,
              "detectedPoint = ", [detectpx0, detectpy0, detectpz0],
              "detectedObjectHandle = ", detectedObjectHandle,
              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

        [
            returnCode,
            detectionState1,
            [detectpx1, detectpy1, detectpz1],
            detectedObjectHandle,
            detectedSurfaceNormalVector
        ] = sim.simxReadProximitySensor(clientID,
                                        r_sensor,
                                        sim.simx_opmode_oneshot_wait)

        detectpx1 = float("%0.2f" % (detectpx1))
        detectpy1 = float("%0.2f" % (detectpy1))
        detectpz1 = float("%0.2f" % (detectpz1))

        print("return code = ", returncode,
              "dectetionstate = ", detectionState1,
              "detectedPoint = ", [detectpx1, detectpy1, detectpz1],
              "detectedObjectHandle = ", detectedObjectHandle,
              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

        [
            returnCode,
            detectionState2,
            [detectpx2, detectpy2, detectpz2],
            detectedObjectHandle,
            detectedSurfaceNormalVector
        ] = sim.simxReadProximitySensor(clientID,
                                        f_sensor,
                                        sim.simx_opmode_oneshot_wait)

        detectpx2 = float("%0.2f" % (detectpx2))
        detectpy2 = float("%0.2f" % (detectpy2))
        detectpz2 = float("%0.2f" % (detectpz2))

        print("return code = ", returncode,
              "dectetionstate = ", detectionState2,
              "detectedPoint = ", [detectpx2, detectpy2, detectpz2],
              "detectedObjectHandle = ", detectedObjectHandle,
              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

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
        print('estou andando reto')
        time.sleep(0.5)

        if detectionState2 == False or (detectionState2 == True and detectpz2 >= 0.3):

            while (detectionState0 == True and detectpz0 <= 0.55) and (detectionState1 == True and detectpz1 <= 0.55):

                print("modo 1: lateral igual, andando reto")
                [
                    returncode,
                    [px1, py1, pz1]
                ] = sim.simxGetObjectPosition(clientID,
                                              robotHandle,
                                              -1,
                                              sim.simx_opmode_oneshot_wait)

                [
                    returnCode,
                    detectionState0,
                    [detectpx0, detectpy0, detectpz0],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                l_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState0,
                      "detectedPoint = ", [detectpx0, detectpy0, detectpz0],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx0 = float("%0.2f" % (detectpx0))
                detectpy0 = float("%0.2f" % (detectpy0))
                detectpz0 = float("%0.2f" % (detectpz0))

                [
                    returnCode,
                    detectionState1,
                    [detectpx1, detectpy1, detectpz1],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                r_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState1,
                      "detectedPoint = ", [detectpx1, detectpy1, detectpz1],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx1 = float("%0.2f" % (detectpx1))
                detectpy1 = float("%0.2f" % (detectpy1))
                detectpz1 = float("%0.2f" % (detectpz1))

                [
                    returnCode,
                    detectionState2,
                    [detectpx2, detectpy2, detectpz2],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                f_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState2,
                      "detectedPoint = ", [detectpx2, detectpy2, detectpz2],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx2 = float("%0.2f" % (detectpx2))
                detectpy2 = float("%0.2f" % (detectpy2))
                detectpz2 = float("%0.2f" % (detectpz2))

                sim.simxSetJointTargetVelocity(clientID,
                                               r_wheel,
                                               v1,
                                               sim.simx_opmode_oneshot_wait)
                sim.simxSetJointTargetVelocity(clientID,
                                               l_wheel,
                                               v1,
                                               sim.simx_opmode_oneshot_wait)
                print('estou andando reto')

                now = time.time()
                dt = now - lastTime
                t = t + dt
                lastTime = now
                print("tempo =", t, "\r")
                if (detectionState0 == False or detectionState1 == False or (detectionState2 == True and detectpz2 < 0.3)):
                    break

            while (detectionState0 == True and detectpz0 > 0.55) or (detectionState1 == True and detectpz1 > 0.55):

                print("modo 2: lateral diferente, andando reto e corrigindo lateral")

                [
                    returnCode,
                    detectionState0,
                    [detectpx0, detectpy0, detectpz0],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                l_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState0,
                      "detectedPoint = ", [detectpx0, detectpy0, detectpz0],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx0 = float("%0.2f" % (detectpx0))
                detectpy0 = float("%0.2f" % (detectpy0))
                detectpz0 = float("%0.2f" % (detectpz0))

                [
                    returnCode,
                    detectionState1,
                    [detectpx1, detectpy1, detectpz1],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                r_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState1,
                      "detectedPoint = ", [detectpx1, detectpy1, detectpz1],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx1 = float("%0.2f" % (detectpx1))
                detectpy1 = float("%0.2f" % (detectpy1))
                detectpz1 = float("%0.2f" % (detectpz1))

                [
                    returnCode,
                    detectionState2,
                    [detectpx2, detectpy2, detectpz2],
                    detectedObjectHandle,
                    detectedSurfaceNormalVector
                ] = sim.simxReadProximitySensor(clientID,
                                                f_sensor,
                                                sim.simx_opmode_oneshot_wait)

                print("return code = ", returncode,
                      "dectetionstate = ", detectionState2,
                      "detectedPoint = ", [detectpx2, detectpy2, detectpz2],
                      "detectedObjectHandle = ", detectedObjectHandle,
                      "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                detectpx2 = float("%0.2f" % (detectpx2))
                detectpy2 = float("%0.2f" % (detectpy2))
                detectpz2 = float("%0.2f" % (detectpz2))

                now = time.time()
                dt = now - lastTime
                t = t + dt
                lastTime = now
                print("tempo =", t, "\r")
                if detectpz0 > 0.55:
                    ang_ori = 0.3
                    while abs(ang_ori) >= 2:

                        print("modo 2.1: corrigindo lateral esquerdo")
                        [
                            returncode,
                            [px1, py1, pz1]
                        ] = sim.simxGetObjectPosition(clientID,
                                                      robotHandle,
                                                      -1, sim.simx_opmode_oneshot_wait)

                        [
                            returncode,
                            [palpha, pbeta, pgamma]
                        ] = sim.simxGetObjectOrientation(clientID,
                                                         robotHandle,
                                                         -1,
                                                         sim.simx_opmode_oneshot_wait)

                        # MHZ: Linter avisa que rad_ori pode ser unbound.
                        if palpha > 0 and pbeta < 0:
                            rad_ori = math.atan(
                                abs(pbeta/palpha))+(-1)*(math.pi/2)
                            ang_ori = (-1)*(((rad_ori*180)/math.pi))
                        elif palpha > 0 and pbeta > 0:
                            rad_ori = math.atan(abs(pbeta/palpha))
                            ang_ori = ((rad_ori*180)/math.pi)+90
                        elif palpha < 0 and pbeta > 0:
                            rad_ori = math.atan(
                                abs(pbeta/palpha))+(-1)*(math.pi/2)
                            ang_ori = (-1)*((rad_ori*180)/math.pi)+180
                        elif palpha < 0 and pbeta < 0:
                            rad_ori = math.atan(abs(pbeta/palpha))
                            ang_ori = ((rad_ori*180)/math.pi)+270
                        print('palpha = ', palpha, 'e pbeta = ', pbeta)
                        print('rad orient = ', rad_ori)
                        print('ang orient = ', ang_ori)
                        kp = 1
                        v2 = 0.2

                        sim.simxSetJointTargetVelocity(clientID,
                                                       r_wheel,
                                                       v1+(kp*v2),
                                                       sim.simx_opmode_oneshot_wait)
                        sim.simxSetJointTargetVelocity(clientID,
                                                       l_wheel,
                                                       v1-(kp*v2),
                                                       sim.simx_opmode_oneshot_wait)
                        print('ang orient = ', ang_ori)
                        print('estou girando parcialmente')
                        [
                            returnCode,
                            detectionState0,
                            [detectpx0, detectpy0, detectpz0],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        l_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState0,
                              "detectedPoint = ", [
                                  detectpx0, detectpy0, detectpz0],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              " detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx0 = float("%0.2f" % (detectpx0))
                        detectpy0 = float("%0.2f" % (detectpy0))
                        detectpz0 = float("%0.2f" % (detectpz0))

                        [
                            returnCode,
                            detectionState1,
                            [detectpx1, detectpy1, detectpz1],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        r_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState1,
                              "detectedPoint = ", [
                                  detectpx1, detectpy1, detectpz1],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx1 = float("%0.2f" % (detectpx1))
                        detectpy1 = float("%0.2f" % (detectpy1))
                        detectpz1 = float("%0.2f" % (detectpz1))

                        [
                            returnCode,
                            detectionState2,
                            [detectpx2, detectpy2, detectpz2],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        f_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState2,
                              "detectedPoint = ", [
                                  detectpx2, detectpy2, detectpz2],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              " detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx2 = float("%0.2f" % (detectpx2))
                        detectpy2 = float("%0.2f" % (detectpy2))
                        detectpz2 = float("%0.2f" % (detectpz2))

                        if (detectionState0 == False or detectionState1 == False) or (detectpz0 <= 0.55 and detectpz1 <= 0.55) or detectpz2 < 0.3:
                            break

                elif detectpz1 > 0.55:
                    ang_ori = 0.3

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
                        if palpha > 0 and pbeta < 0:
                            rad_ori = math.atan(
                                abs(pbeta/palpha))+(-1)*(math.pi/2)
                            ang_ori = (-1)*(((rad_ori*180)/math.pi))
                        elif palpha > 0 and pbeta > 0:
                            rad_ori = math.atan(abs(pbeta/palpha))
                            ang_ori = ((rad_ori*180)/math.pi)+90
                        elif palpha < 0 and pbeta > 0:
                            rad_ori = math.atan(
                                abs(pbeta/palpha))+(-1)*(math.pi/2)
                            ang_ori = (-1)*((rad_ori*180)/math.pi)+180
                        elif palpha < 0 and pbeta < 0:
                            rad_ori = math.atan(abs(pbeta/palpha))
                            ang_ori = ((rad_ori*180)/math.pi)+270

                        print('palpha = ', palpha, 'e pbeta = ', pbeta)
                        print('rad orient = ', rad_ori)
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
                        [
                            returnCode,
                            detectionState0,
                            [detectpx0, detectpy0, detectpz0],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        l_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState0,
                              "detectedPoint = ", [
                                  detectpx0, detectpy0, detectpz0],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx0 = float("%0.2f" % (detectpx0))
                        detectpy0 = float("%0.2f" % (detectpy0))
                        detectpz0 = float("%0.2f" % (detectpz0))

                        [
                            returnCode,
                            detectionState1,
                            [detectpx1, detectpy1, detectpz1],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        r_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState1,
                              "detectedPoint = ", [
                                  detectpx1, detectpy1, detectpz1],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              "detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx1 = float("%0.2f" % (detectpx1))
                        detectpy1 = float("%0.2f" % (detectpy1))
                        detectpz1 = float("%0.2f" % (detectpz1))

                        [
                            returnCode,
                            detectionState2,
                            [detectpx2, detectpy2, detectpz2],
                            detectedObjectHandle,
                            detectedSurfaceNormalVector
                        ] = sim.simxReadProximitySensor(clientID,
                                                        f_sensor,
                                                        sim.simx_opmode_oneshot_wait)

                        print("return code = ", returncode,
                              "dectetionstate = ", detectionState2,
                              "detectedPoint = ", [
                                  detectpx2, detectpy2, detectpz2],
                              "detectedObjectHandle = ", detectedObjectHandle,
                              " detectedSurfaceNormalVector = ", detectedSurfaceNormalVector)

                        detectpx2 = float("%0.2f" % (detectpx2))
                        detectpy2 = float("%0.2f" % (detectpy2))
                        detectpz2 = float("%0.2f" % (detectpz2))

                        if (detectionState0 == False or detectionState1 == False) or (detectpz0 <= 0.55 and detectpz1 <= 0.55) or detectpz2 < 0.3:
                            break

        if (detectionState2 == True and detectpz2 < 0.3):

            time.sleep(0.5)
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

            if detectionState0 == True and detectionState1 == True:

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

                    if palpha > 0 and pbeta < 0:
                        rad_ori = math.atan(abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*(((rad_ori*180)/math.pi))
                    elif palpha > 0 and pbeta > 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+90
                    elif palpha < 0 and pbeta > 0:
                        rad_ori = math.atan(abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*((rad_ori*180)/math.pi)+180
                    elif palpha < 0 and pbeta < 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+270

                    print('palpha = ', palpha, 'e pbeta = ', pbeta)
                    print('rad orient = ', rad_ori)
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
            time.sleep(0.5)

            if detectionState0 == False:
                while abs(ang_ori - 90) > 3:
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

                    if palpha > 0 and pbeta < 0:
                        rad_ori = math.atan(abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*(((rad_ori*180)/math.pi))
                    elif palpha > 0 and pbeta > 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+90
                    elif palpha < 0 and pbeta > 0:
                        rad_ori = math.atan(abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*((rad_ori*180)/math.pi)+180
                    elif palpha < 0 and pbeta < 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+270

                    print('palpha = ', palpha, 'e pbeta = ', pbeta)
                    print('rad orient = ', rad_ori)
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

            if detectionState1 == False:
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

                    if palpha > 0 and pbeta < 0:
                        rad_ori = math.atan(
                            abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*(((rad_ori*180)/math.pi))
                    elif palpha > 0 and pbeta > 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+90
                    elif palpha < 0 and pbeta > 0:
                        rad_ori = math.atan(
                            abs(pbeta/palpha))+(-1)*(math.pi/2)
                        ang_ori = (-1)*((rad_ori*180)/math.pi)+180
                    elif palpha < 0 and pbeta < 0:
                        rad_ori = math.atan(abs(pbeta/palpha))
                        ang_ori = ((rad_ori*180)/math.pi)+270

                    print('palpha = ', palpha, 'e pbeta = ', pbeta)
                    print('rad orient = ', rad_ori)
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

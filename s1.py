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


import sim
import time
import math

def lersensor(clientID,sensor):
  [
    returnCode,
    detectionState,
    [detectpx, detectpy, detectpz],
    detectedObjectHandle,
    detectedSurfaceNormalVector
  ] = sim.simxReadProximitySensor(clientID,sensor,sim.simx_opmode_oneshot_wait)

  detectpx = float("%0.2f" % (detectpx))
  detectpy = float("%0.2f" % (detectpy))
  detectpz = float("%0.2f" % (detectpz))
  return detectionState, detectpx, detectpy, detectpz

thet = 0
x_glob = 0
y_glob = 0

def odomet(phid, phie):
    r = 0.195/2
    l = 0.331
    v = r*(phid+phie)/2
    omega =  r*(phid-phie)/(l)
    return v, omega

def mov_dir(handleR, handleL, client,v,thet):
    vl,vang=odomet(-v,v)
    tempo = abs(math.pi/(2*vang))
    thet+=vang*tempo
    sim.simxSetJointTargetVelocity(client, handleR, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, v, sim.simx_opmode_oneshot)
    time.sleep(tempo)
    sim.simxSetJointTargetVelocity(client, handleR, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, 0, sim.simx_opmode_oneshot)
    return thet

def mov_esq(handleR, handleL, client,v,thet):
    vl,vang=odomet(v,-v)
    tempo = abs(math.pi/(2*vang))
    thet+=vang*tempo
    sim.simxSetJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, -v, sim.simx_opmode_oneshot)
    time.sleep(tempo)
    sim.simxSetJointTargetVelocity(client, handleR, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, 0, sim.simx_opmode_oneshot)
    return thet
    
def mov_tras(handleR, handleL, client,v,thet):
    vl,vang=odomet(v,-v)
    sim.simxSetJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, -v, sim.simx_opmode_oneshot)
    tempo = abs(math.pi/(vang))
    thet+=vang*tempo
    time.sleep(tempo-tempo/40)
    sim.simxSetJointTargetVelocity(client, handleR, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, 0, sim.simx_opmode_oneshot)
    return thet

def vai_reto(handleR, handleL, client,v,v2,thet,x,y):
    #anda reto
    sim.simxSetJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(client, handleL, v2, sim.simx_opmode_oneshot)
    vl,vang=odomet(v,v2)
    x +=vl*0.1*math.cos(thet)
    y +=vl*0.1*math.sin(thet)
    time.sleep(0.1)
    return x, y, thet

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
    distanciaL=0
    distanciaR=0
    print("tempo do momento:")
    while px1 != 4 and py1 != -4:
        # código de tempo
        now = time.time()
        dt = now - lastTime

        t = t + dt
        lastTime = now
        # Velocidade básica (linear)
        v = 0.7
        v1 = 4

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
            if detectionStateR and distanciaR-detectpz1>0.001:
                 x,y,thet=vai_reto(r_wheel, l_wheel, clientID,v1+0.1,v1,thet,x_glob,y_glob)
            elif detectionStateL and distanciaL-detectpz0>0.001:
                 x,y,thet=vai_reto(r_wheel, l_wheel, clientID,v1,v1+0.1,thet,x_glob,y_glob)
            elif detectionStateR and distanciaR-detectpz1<-0.001:
                 x,y,thet=vai_reto(r_wheel, l_wheel, clientID,v1-0.1,v1,thet,x_glob,y_glob)
            elif detectionStateL and distanciaL-detectpz0<-0.001:
                 x,y,thet=vai_reto(r_wheel, l_wheel, clientID,v1,v1-0.1,thet,x_glob,y_glob)
            print("distancia em parede",distanciaR-detectpz1)
            distanciaR=detectpz1
            distanciaL=detectpz0          
            x,y,thet=vai_reto(r_wheel, l_wheel, clientID,v1,v1,thet,x_glob,y_glob)
            print('estou andando reto')
        time.sleep(0.05)

        if (detectionStateF == True and detectpz2 < 0.7):

            sim.simxSetJointTargetVelocity(clientID,
                                           l_wheel,
                                           0,
                                           sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID,
                                           r_wheel,
                                           0,
                                           sim.simx_opmode_oneshot)
            print('estou parando por condições possíveis')
            print("modo 3: objeto frontal detectado, mudar direção")

            if detectionStateL == True and detectionStateR == True:
                    print("modo 3.0: virar 180 graus!")
                    thet=mov_tras(r_wheel, l_wheel, clientID,v,thet)
            elif detectionStateR == False: 
                    print("modo 3.1: virar 270 graus! virando para direita!")
                    thet=mov_dir(r_wheel, l_wheel, clientID,v,thet)
            elif detectionStateL == False:
                    print("modo 3.2: virar 90 graus! virando para esquerda!")
                    thet=mov_esq(r_wheel, l_wheel, clientID,v,thet)

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
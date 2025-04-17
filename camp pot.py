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

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
import random
#import matplotlib


print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)
    
    # variáveis e handle para o robo e o objetivo
    robotname = 'Pioneer_P3DX'
    returnCode, robotHandle = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)
    print('Handle return code:',(returnCode, robotHandle))     


    # Handle para as juntas das RODAS
    returnCode, l_wheel = sim.simxGetObjectHandle(clientID, '_leftMotor', sim.simx_opmode_oneshot_wait)
    print('Handle return code:',(returnCode, l_wheel))
    returnCode, r_wheel = sim.simxGetObjectHandle(clientID, '_rightMotor', sim.simx_opmode_oneshot_wait)    
    print('Handle return code:',(returnCode, r_wheel)) 

    #mostrar os dados da posição e orientação

    [returncode, [px1,py1,pz1]] = sim.simxGetObjectPosition(clientID, robotHandle, -1, sim.simx_opmode_oneshot_wait)        
    print('Robot Pos: ', px1,py1,pz1)
    print('robot pos return code:',returnCode)
    [returncode, [palpha, pbeta, pgamma]] = sim.simxGetObjectOrientation(clientID,robotHandle,-1,sim.simx_opmode_oneshot_wait)
    print('robot orient: ', palpha, pbeta)

    print('robot orient return code:',returncode)

    #print de coordenadas
    print('as coordenadas da origem são: ',px1,py1)    
    print('as orientações do robot: ',palpha,pbeta,pgamma)
    time.sleep(2)
    print(returncode)

    # Lembrar de habilitar o 'Real-time mode'
    t = 0
    startTime=time.time()
    lastTime = startTime

    #mapa do problema
    map = {[1,1,1,1,1,1,1,1,1,1,1],
	   [1,0,0,0,1,0,0,0,0,0,1],
           [1,0,1,0,1,0,1,1,1,0,1],
           [1,0,1,0,0,0,0,0,1,0,1],
           [1,0,1,1,1,1,1,0,1,1,1],
           [1,0,0,0,1,0,0,0,0,0,1],
           [1,0,1,1,1,0,1,0,1,0,1],
           [1,0,0,0,0,0,1,0,1,0,1],
           [1,0,1,1,1,1,1,0,1,1,1],
           [1,0,0,0,0,0,1,0,0,0,1],
	   [1,1,1,1,1,1,1,1,1,1,1]}

    campo_pot = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0]]
    
    for i in range(8,0):
        for j in range(8,0):
            somax = 8
            somay = 8
            passo = 0
            inimap = map[somax][somay]
            endmap = map[i][j]
            
            if endmap == 1: 
                campo_pot[i][j] == 99
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

                    elif 
            


        now = time.time()
        dt = now - lastTime
        t = t + dt
        lastTime = now
        print("tempo =",t, "\r")


    # Parando o robo    
    sim.simxSetJointTargetVelocity(clientID, r_wheel, 0, sim.simx_opmode_oneshot_wait)
    sim.simxSetJointTargetVelocity(clientID, l_wheel, 0, sim.simx_opmode_oneshot_wait)   
    print('estou parando: 3 ')

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'goodbye CoppeliaSim!',sim.simx_opmode_oneshot)
    print('goodbye Coppeliasim!')

    # Parando a simulação     
    sim.simxStopSimulation(clientID,sim.simx_opmode_blocking) 
    print('parando a simulação')
    
    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')


import time
import sim
import math
#info do robo
raio_rodas = 195/2*10e-4
l = 381*10e-4
thet = 0
x_glob = 0
y_glob = 0

def odomet(r, phid, phie, l):
    v = r*(phid+phie)/2
    omega =  r*(phid-phie)/(l)
    return v, omega

def mov_dir(vang, handleR, handleL, client):
    # mudar para a direita
    # sleep
    # return vazio
    sim.setJointTargetVelocity(client, handleR, -vang, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, vang, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/(4*vang)
    time.sleep(tempo)
    return

def mov_esq(vang, handleR, handleL, client):
    # mudar para a esquerda 
    # sleep
    # return vazio
    sim.setJointTargetVelocity(client, handleR, vang, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, -vang, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/(4*vang)
    time.sleep(tempo)
    return
    
def mov_tras(vang, handleR, handleL, client):
    # gira 180º
    # sleep
    # return vazio
    sim.setJointTargetVelocity(client, handleR, vang, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, -vang, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/(2*vang)
    time.sleep(tempo)
    return

def vai_reto(vang, handleR, handleL, client):
    #anda reto
    sim.setJointTargetVelocity(client, handleR, -vang, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, vang, sim.simx_opmode_oneshot_wait)
    time.sleep(0.25)
    return

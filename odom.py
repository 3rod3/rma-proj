import time
import sim
import math
#info do robo
raio_rodas = 195/2*10e-4
l = 381*10e-4
thet = 0
x_glob = 0
y_glob = 0

def odomet(phid, phie):
    r = 195/2*10e-4
    l = 381*10e-4
    v = r*(phid+phie)/2
    omega =  r*(phid-phie)/(l)
    return v, omega

def mov_dir(handleR, handleL, client,v,thet):
    # mudar para a direita
    # sleep
    # return vazio
    vl,vang=odomet(-v,v)
    sim.setJointTargetVelocity(client, handleR, -v, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, v, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/(2*vang)
    thet+=vang*tempo
    time.sleep(tempo)
    return thet

def mov_esq(handleR, handleL, client,v,thet):
    # mudar para a esquerda 
    # sleep
    # return vazio
    vl,vang=odomet(v,-v)
    sim.setJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, -v, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/(2*vang)
    thet+=vang*tempo
    time.sleep(tempo)
    return thet
    
def mov_tras(handleR, handleL, client,v,thet):
    # gira 180º
    # sleep
    # return vazio
    vl,vang=odomet(v,-v)
    sim.setJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, -v, sim.simx_opmode_oneshot_wait)
    tempo = math.pi/vang
    thet+=vang*tempo
    time.sleep(tempo)
    return thet

def vai_reto(handleR, handleL, client,v,thet,x,y):
    #anda reto
    vl,vang=odomet(v,v)
    sim.setJointTargetVelocity(client, handleR, v, sim.simx_opmode_oneshot_wait)
    sim.setJointTargetVelocity(client, handleL, v, sim.simx_opmode_oneshot_wait)
    x +=vl*0.25*math.cos(thet)
    y +=vl*0.25*math.sin(thet)
    time.sleep(0.25)
    return x,y

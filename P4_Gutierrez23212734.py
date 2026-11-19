"""
Práctica 4: Sistema endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Sara Gutierrez Hernandez
Número de control: 23212734
Correo institucional: l23212734@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# pip install numpy control matplotlib

#Librerias
import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy import signal
import control as ctrl
import pandas as pd

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,5,1E-3,10,5
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u = np.ones(N)

# Componentes del circuito RLC
def endocrino(C,R2):
    R1,L = 1E3,100E-3
    num = [L,R2]
    den = [R1*L*C,L+R1*R2*C,R1+R2]
    sys = ctrl.tf(num,den)
    polos = np.roots(den)
    return sys,polos

# Función de transferencia de control
C,R2 = 1E-6,100E3
sysControl,L = endocrino(C,R2)
print(f"Función de transferencia del control: {sysControl}")
print(f"Polos del sistema: l1 = {L[0]:.3e}, l2 = {L[1]:.3e}\n")

# Función de transferencia de caso
C,R2 = 1000E-6,1E3
sysCaso,L = endocrino(C,R2)
print(f"Función de transferencia del caso: {sysCaso}")
print(f"Polos del sistema: l1 = {L[0]:.3e}, l2 = {L[1]:.3e}\n")

# Respuesta del sistema en lazo abierto
_,Fsx = ctrl.forced_response(sysControl,t,u,x0)
_,Fsy = ctrl.forced_response(sysCaso,t,u,x0)

# Error en estado estacionario
essControl = 1-ctrl.dcgain(sysControl)
essCaso = 1-ctrl.dcgain(sysCaso)
print(f"Error estacionario del control: {essControl:.6f}")
print(f"Error estacionario del caso: {essCaso:.6f}")
print(f"Diferencia final: {essCaso-essControl:.6f}\n")

# Controlador PI
def controlador(kI,kP,sys):
    Cr = 1E-6
    Re = 1/(Cr*kI)
    Rr = kP*Re
    numPID = [Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

casoPID = controlador(15701.1743144083,45654430.6926081,sysCaso)
print(f"Función de transferencia del sistema endocrino en lazo cerrado: {casoPID}\n")

# Respuesta del sistema en lazo cerrado
_,PI = ctrl.forced_response(casoPID,t,Fsx,x0)

# Colores
clr1 = np.array([66, 91, 154])/255
clr2 = np.array([40, 122, 116])/255
clr3 = np.array([151, 40, 40])/255
clr4 = np.array([128,81,255])/255

# Gráfica
fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'

plt.plot(t,u,'-',linewidth=0.7,color=clr1,label='Ve(t): Entrada')
plt.plot(t,Fsx,'-',linewidth=1,color=clr2,label='Vs(t): Control')
plt.plot(t,Fsy,'-',linewidth=1,color=clr3,label='Vs(t): Caso')
plt.plot(t,PI,':',linewidth=1,color=clr4,label='PID')

plt.xlim(0,5); plt.xticks(np.arange(0,5.1,0.5))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.11,0.1))
plt.xlabel('t [s]')
plt.ylabel('Vs(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
fg.savefig('Caso_python.pdf',bbox_inches='tight')
plt.show()
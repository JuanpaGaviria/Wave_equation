#This code compares the explicit, implicit and analytical solution for a standing wave
#Libraries
import matplotlib.pyplot as plt
import numpy as np
############################## Implicit method ##########################################
#######################################################################
#Physic parameters 
bulk_modulus= 1.
density=1.
velocity2=bulk_modulus/density #velocity^2
vel=0.
amplitud=2.
period=1.5
########################################################################
#Mesh parameters 
n=100
L=1
#Spacial parameters
dx=L/(n-1)
xnodes=np.linspace(0,L,n)
#Time parameters
t=100
ntpasos=10000
dt=t/(ntpasos-1)
#dt=0.2e-6
#########################################################################
#Vectors and matrix for implicit method
Ai=np.zeros((n-2,n-2))
Bi=np.zeros(n-2)
Uj0i=np.zeros(n-2) #Ujpresent
Uj1i=np.zeros(n-2) #Ujfuture
Uj_1i=np.zeros(n-2) #Ujpast
Hi=np.zeros((n,ntpasos+1)) #In this matrix the mesh solution of each iteration is saved
                          
########################################################################
#Boundary conditions
Uleft=0
Uright=0
#Initial condition
xi=np.linspace(0,L,n-2) #x=xnodes[1:4:1] indexacion de arreglos (slicing)
Uj0i=np.sin(np.pi*xi)

#Saving initial condition in matrix H 
Uj0ti=np.hstack([Uleft, Uj0i, Uright])
Hi[:,0]=Uj0ti

#Coeficiente de constantes
r=bulk_modulus*dt**2/(density*dx**2)


#Esquema implicito: Armado 
for j in range(0,ntpasos):
    if j==0: 
        Uleft=0
        for i in range(0,n-1):
            if i==0:
                Ai[i,i]=1+2*r
                Ai[i,i+1]=-r
                Bi[i]=Uj0i[i]+r*Uleft+vel*dt
            if i>0 and i<n-3:
                Ai[i,i-1]=-r
                Ai[i,i]=1+2*r
                Ai[i,i+1]=-r
                Bi[i]=Uj0i[i]+vel*dt
            if i==n-3:
                Ai[i,i-1]=-r
                Ai[i,i]=1+2*r
                Bi[i]=Uj0i[i]+vel*dt+r*Uright
        Uj1i=np.linalg.solve(Ai,Bi)
        Uj1ti=np.hstack([Uleft, Uj1i, Uright])
        Hi[:,j+1]=Uj1ti[:]
        Uj_1i=Uj0i
        Uj0i=Uj1i
        
    if j>0: 
        for i in range(0,n-1):
            if i==0:
                Ai[i,i]=1+2*r
                Ai[i,i+1]=-r
                Bi[i]=2*Uj0i[i]-Uj_1i[i] +r*Uleft
            if i>0 and i<n-3:
                Ai[i,i-1]=-r
                Ai[i,i]=1+2*r
                Ai[i,i+1]=-r
                Bi[i]=2*Uj0i[i]-Uj_1i[i]
            if i==n-3:
                Ai[i,i-1]=-r
                Ai[i,i]=1+2*r
                Bi[i]=2*Uj0i[i]- Uj_1i[i] +r*Uright
        Uj1i=np.linalg.solve(Ai,Bi)
        Uj1ti=np.hstack([Uleft, Uj1i, Uright])
        Hi[:,j+1]=Uj1ti[:]
        Uj_1i=Uj0i
        Uj0i=Uj1i
############################## Explicit method ##########################################
#Defining vectors for solution 
uj1e=np.zeros(n)
uj0e=np.zeros(n)
uj_1e=np.zeros(n)
He=np.zeros((n,ntpasos+1))


#Initial conditions
v0=0
    #Defining space vector for the calculation of the initial deformation 
xe=np.linspace(0,L,n)
uj0e=np.sin(np.pi*xe) 

#Saving initial condition in matrix H 
He[:,0]=uj0e

#t=0.3
#Solving the proble through FDM 

for j in range(ntpasos):
#For first time iteration
    if j==0: 
        for i in range(n):
          if i==0:
              uj1e[i]=0

          if i>0 and i<n-1: #Intern nodes
            uj1e[i]=(((dt**2*velocity2)/(2*dx**2))*(uj0e[i+1]-2*uj0e[i]+uj0e[i-1]))\
                +uj0e[i]-(dt*v0)
            
          if i==n-1:
            uj1e[i]=0
#For above first time iteration
    if j>0: 
        for i in range(n):
          if i==0:
             uj1e[i]=0
          if i>0 and i<n-1: #Intern nodes
            uj1e[i]=(((dt**2*velocity2)/(dx**2))*(uj0e[i+1]-2*uj0e[i]+uj0e[i-1]))\
                +2*uj0e[i]-uj_1e[i]
          if i==n-1:
            uj1e[i]=0

    He[:,j+1]=uj1e  #Saving space vector in matrix H
    uj_1e[:]=uj0e  #time update
    uj0e[:]=uj1e

#####################Analytical solution##########################################
xa=np.linspace(0,1,n)
Ha=np.zeros((n,ntpasos+1))
uj1a=np.zeros(n)
uj0a=np.zeros(n)
uj0a=np.sin(np.pi*xa)
Ha[:,0]=uj0a
for j in range (0,ntpasos):
    uj1a=np.sin(np.pi*xa)*np.cos(np.pi*j*dt)
    Ha[:,j+1]=uj1a

#Saving the results
np.savetxt('explicit_solution.txt',He)
np.savetxt('implicit_solution.txt',Hi)
np.savetxt('analytical_solution.txt',Ha)

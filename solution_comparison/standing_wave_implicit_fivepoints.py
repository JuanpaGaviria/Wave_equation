#Standing wave solved by implicit method-five points
#######################################################################
#Libraries
import matplotlib.pyplot as plt
import numpy as np
#######################################################################
#Physic parameters 
bulk_modulus= 1.
density=1.
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
#dt=0.2e-4
#########################################################################
#Vectors and matrix for implicit method
A=np.zeros((n-2,n-2))
B=np.zeros(n-2)
Uj0=np.zeros(n-2) #Ujpresent
Uj1=np.zeros(n-2) #Ujfuture
Uj_1=np.zeros(n-2) #Ujpast
H=np.zeros((n,ntpasos+1)) #In this matrix the mesh solution of each iteration is saved
                          
########################################################################
#Boundary conditions
Uleft=0
Uright=0
#Initial condition
x=np.linspace(0,L,n-2) #x=xnodes[1:4:1] indexacion de arreglos (slicing)
Uj0=np.sin(np.pi*x)

#Saving initial condition in matrix H 
Uj0t=np.hstack([Uleft, Uj0, Uright])
H[:,0]=Uj0t

#Coeficiente de constantes
r=bulk_modulus*dt**2/(density*dx**2)

#Esquema implicito: Armado 
for j in range (0,ntpasos):
    if j==0: 
        for i in range(0,n-1):
            if i==0:
                A[i,i]=1+2*r
                A[i,i+1]=-r
                B[i]=Uj0[i]+r*Uleft+vel*dt
            if i==1:
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                A[i,i+2]=r
                B[i]=Uj0[i]+vel*dt-r*Uleft
            if i>1 and i<n-4:
                A[i,i-2]=r
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                A[i,i+2]=r
                B[i]=Uj0[i]+vel*dt
            if i==n-4:
                A[i,i-2]=r
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                B[i]=Uj0[i]+vel*dt+r*Uright
            if i==n-3:
                A[i,i-1]=-r
                A[i,i]=1+2*r
                B[i]=Uj0[i]+vel*dt+r*Uright
        Ainv=np.linalg.pinv(A)
        Uj1=np.dot(Ainv,B)
        Uj1t=np.hstack([Uleft, Uj1, Uright])
        H[:,j+1]=Uj1t[:]
        Uj_1=Uj0
        Uj0=Uj1
        
    if j>0: 
        for i in range(0,n-1):
            if i==0:
                A[i,i]=1+2*r
                A[i,i+1]=-r
                B[i]=2*Uj0[i]-Uj_1[i] +r*Uleft
            if i==1:
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                A[i,i+2]=r
                B[i]=2*Uj0[i]-Uj_1[i]-r*Uleft
            if i>1 and i<n-4:
                A[i,i-2]=r
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                A[i,i+2]=r
                B[i]=2*Uj0[i]-Uj_1[i]
            if i==n-4:
                A[i,i-2]=r
                A[i,i-1]=-16*r
                A[i,i]=1+30*r
                A[i,i+1]=-16*r
                B[i]=2*Uj0[i]-Uj_1[i]-r*Uright
            if i==n-3:
                A[i,i-1]=-r
                A[i,i]=1+2*r
                B[i]=2*Uj0[i]-Uj_1[i] +r*Uright
        Ainv=np.linalg.pinv(A)
        Uj1=np.dot(Ainv,B)
        Uj1t=np.hstack([Uleft, Uj1, Uright])
        H[:,j+1]=Uj1t[:]
        Uj_1=Uj0
        Uj0=Uj1
    
#Saving the results
np.savetxt('implicit_solution_fivepoints.txt',H)

for i in range(0,ntpasos+1):
    plt.cla()# borra pantalla anterior del plot
    plt.xlim(0,1.)
    plt.ylim(-2,2.)
    plt.plot(xnodes,H[:,i],color='r')
    titulo= 'propagation'
    plt.title(titulo)
    plt.grid()
    plt.pause(0.0000000000001)
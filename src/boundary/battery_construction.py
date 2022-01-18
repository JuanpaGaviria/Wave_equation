indexes=[1,2,3]
vueltas=2
capas=2*int(len(indexes))*vueltas
interfaces=capas-1
if vueltas == 0:
    capas=int(len(indexes))
    interfaces=1

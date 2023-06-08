import multiprocessing as mp
import time

def sequence(nb_dispo):
    m=3
    for j in range(m):
        demande(nb_dispo,j)
        #traitement k
        time.sleep(2)
        #retour k
        rendre(nb_dispo,j)
def demande(nb_dispo,k):
    verrou.acquire()
    while nb_dispo<k:
        verrou.release()
        semat.acquire
    nb_dispo -= k
    
def rendre(nb_dispo,k):
    verrou.acquire()
    nb_dispo += k
    verrou.release()

def controleur(max,billes_dispo):
    while True:
        if max >=billes_dispo and billes_dispo>0:
            print("Controle OK")
        else:
            print("Controle ECHOUE")
        time.sleep(1)
        
if __name__ == "__main__" :
    N=4
    nb_max_billes = 9
    # verrou 
    verrou = mp.Lock()
    # semaphore d'attente
    semat= mp.Semaphore(1)
    # Variable partagé du nombre de billes disponibles
    sac_billes = mp.Value("i",nb_max_billes) #"i " indique un entier => Vinitiale =9
    mes_process = [0 for i in range(N)]
    for i in range(N):  # Lancer   Nb_process  processus
        mes_process[i] = mp.Process(target=(sequence), args= (i))
        mes_process[i].start()

    for i in range(N): mes_process[i].join()
    
    cont = mp.Process(target = controleur,args=())
    cont.start()
    cont.join()
    
    time.sleep(10)
    
    #attente fin process
    cont.terminate()
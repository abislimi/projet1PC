# Author : Corentin Carisey
# Date de debut : 06/06/23
# Derniere modification : 06/06
# A Faire :
#  1 Realiser le système de calcul avec les 3 calculateurs
#  2 Saisie protégé lors de l'ecriture dans la file demande
#
#
#
import time,os,random
import multiprocessing as mp

def fils_calculette(id ):
    
    while True :
        print("Bonjour du Fils", id)
        cmd = demande.get()
        print("Le fils a recu ", cmd)
        res=eval(cmd)
        print("Dans fils, le résultat =", res)
        resultat.put(res)
        print("Le fils a envoyé", res)
        time.sleep(1)



def demandeur():
    # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
    while True :
        opd1 = random.randint(1,10)
        opd2 = random.randint(1,10)
        operateur=random.choice(["+", "-", "*", "/"])
        str_commande = str(opd1) + operateur + str(opd2)
        demande.put(str_commande.encode())
        print("Le père va demander à faire : ", str_commande)
        res = resultat.get(False)
        print("Le Pere a recu ", res)
        print("-"* 60)
        time.sleep(1)


if __name__ == "__main__" :

    
    #Init Queu
    demande = mp.Queue()
    resultat = mp.Queue()
    
    # Init process demandeur
    dem = mp.Process(target=(demandeur),args=())
    #Démmarage demande
    dem.start()
    dem.join()
    #Init Calculateur
    nb_calc = 3
    mes_calc = [0 for i in range(nb_calc)]
    
    # init process calculateurs
    for i in range(nb_calc):  
        mes_calc[i] = mp.Process(target=fils_calculette, args= (str(i)))
        mes_calc[i].start()
    
    # Démmarage calculateur
    for i in range(nb_calc): mes_calc[i].join()
    

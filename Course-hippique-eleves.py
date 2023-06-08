# Cours hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagant, ... ...


# Programmeur : Carisey Corentin
# Date de DEBUT 25 Mai 2023
# Dernière modif
#A Faire : 
# -ADAPTER arbitre au nouvel affichage
#

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# Nov 2021
# Course Hippique (version élèves)
# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

#-------------------------------------------------------
import multiprocessing as mp
 
import os, time,math, random, sys, ctypes, array

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
             CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !


# La tache d'un cheval
def un_cheval(repere_cheval : int, keep_running) : # repere_cheval commence à 0
    col=1
    while col < LONGEUR_COURSE and keep_running.value :
        for i in range(3) :
            move_to(repere_cheval*4+i,col)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            # Section critique
            mutex.acquire()
            if i == 0 : print("_______\/")
            if i == 1 : print( " /---- _.\ " )
            if i == 2 : print("/|__"+chr(ord('A')+repere_cheval)+"___/")
            if i == 3 : print("/\ /\ ") 
            mutex.release()
        en_couleur(lyst_colors[repere_cheval%len(lyst_colors)])

        tableau[repere_cheval] = col         #Chaque cheval ajoute sa position au tableau
        col+=1
        time.sleep(0.1 * random.randint(1,5))

#------------------------------------------------
# La partie principale :
def course_hippique(keep_running) :

    
 
    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]
    

    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,))
        mes_process[i].start()
    mes_process[0]
    move_to(Nb_process+10, 1)




    for i in range(Nb_process): mes_process[i].join()

    move_to(24, 1)
    curseur_visible()
def arbitre():
    #Affichage 1er et Dernier
    lst2 = () #Tableau final

    while keep_running.value :
        lst =(tableau[:]) #Tableau des positions en temps réel
        
        move_to(Nb_process*4+1,0)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        premier_cheval = chr(lst.index(max(lst))+65)            # Recuperation du cheval a partir de sa position dans la liste
        dernier_cheval = chr(lst.index(min(lst))+65)            # Chr traduit un entier en une lettre
        
        #Section critique 
        mutex.acquire()
        print("Premier cheval : ",premier_cheval)
        print("Dernier cheval :",dernier_cheval)
        mutex.release()     #Protection d'affichage
        
        
        #Detection de l'arrivée du premier cheval  
        # On considère que la course est terminé lorsque le permier cheval franchit la ligne.
        for i in range(len(lst)):
            if lst[i] == LONGEUR_COURSE-1: #Detection fin de course
                lst2 = lst                  #Captage du classement en fin de course
                keep_running == False
                for i in range(Nb_process): 
                    mes_process[i].terminate() #Fermeture des process

        # Recherche des exaequo   
        
        #move_to(Nb_process+2,0)
        #print("Chevaux exaequo",dup )
        
        time.sleep(0.3)


# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
         
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    LONGEUR_COURSE = 50 # Tout le monde aura la même copie (donc no need to have a 'value')
    keep_running=mp.Value(ctypes.c_bool, True)

    # course_hippique(keep_running)
    
    Nb_process=4
    mes_process = [0 for i in range(Nb_process)]
    
    #Initialisation du verrou
    mutex = mp.Lock()
    
    #Tableau des chevaux
    tableau = mp.Array("i",Nb_process)
    
    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer   Nb_process  processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,))
        mes_process[i].start()
    
 
    #Process arbitre
    P_arbitre = mp.Process(target=arbitre, args=())
    P_arbitre.start()
    P_arbitre.join()


    for i in range(Nb_process): mes_process[i].join()

    move_to(24, 1)
    curseur_visible()
    

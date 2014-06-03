#!/usr/bin/python

import tweepy
import webbrowser    #mi serve per far aprire la finestra del browser sull'url per l'autenticazione
import info          #file con tutte le funzioni (?) create da noi
import sys
import ConfigParser  #parser per i file di configurazione
import argparse      #parser per i parametri passati all'avvio
import listatweet
import time          #per il rilevamento del tempo di sistema


def main():
    
    time_start = time.time()    #salva in time_start il tempo di sistema all'avvio del main.
    
    argomenti = info.parametri_avvio()		#gestisce le opzioni passate all'avvio.
    nuova_registrazione = False
    if argomenti.nuovotweet:
        listatweet.aggiungitweet()
        exit()
       
    if argomenti.registra:
        nuova_registrazione = True 
 
# crea il file di config se non esiste
    try:
        open('./config.cfg', 'r')
    except:
        info.creazione()			#crea il file di configurazione
        nuova_registrazione = True

    if nuova_registrazione == True:
        info.configura()			#configura il file di creazione
        
    auth = info.autenticazione()		#crea la "chiave" auth, per aprire le API twitter
        
    bot = tweepy.API(auth)			#usa la chiave per aprire le API, in bot ci sono le API tweepy
            
# sta roba e' piuttosto inutile, ma e' solo per provare. In pratica stampa a video in modo
# piuttosto illeggibile il testo dei post degli utenti seguiti dal nostro bot.

    config = ConfigParser.RawConfigParser()	#serve per prelevare il nome utente dal file di config
    config.read('./config.cfg')			#apre il file di configurazione per leggere il nome dell'utente di cui stampa i tweet.
    timeline = bot.home_timeline()
    print 'STO STAMPANDO I TWEET DI: ' + config.get('utente', 'nome_utente')
    i = 0
    for post in timeline:
#        print post.id,
        i+=1
        print i,
        print post.user.name + ' (' + post.user.lang + '):',
        print post.text + '\n\n' 
    
#    print dir(post.user)
    
#faccio stampare alla fine il nome utente, cosi non devo ritornare in cima per controllare se viene stampato correttamente.
    print 'STO STAMPANDO I TWEET DI: ' + config.get('utente', 'nome_utente') + '\n'
    
#prova della ricerca di un hashtag
    trovati = bot.search('#dimmidino')
    for post in trovati:
        print 'L\'utente ' + post.user.name + ' ha scritto:\n' + post.text + '\n\n'
        
#prova della funzione tempo
    tempo = info.time_up(time_start)
    print "Giorni: %d\nOre: %d\nMinuti: %d\nSecondi: %d\n" % (tempo.days, tempo.hours, tempo.minutes, tempo.seconds)


if __name__ == '__main__':
    main()

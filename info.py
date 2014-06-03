#!/usr/bin/env python

import ConfigParser
import tweepy
import webbrowser
import argparse      #parser per i parametri passati all'avvio
import time

class t_date:   #classe creata per le funzioni time.
    pass

def creazione():
#crea il file di configurazione con i parametri impostati a 0
    
    config = ConfigParser.RawConfigParser()

    config.add_section('applicazione')
    config.add_section('utente')
    
    config.set('applicazione', 'consumer_token', '0')
    config.set('applicazione', 'consumer_secret', '0')
    config.set('utente', 'nome_utente', '0')
    config.set('utente', 'key', '0')
    config.set('utente', 'secret', '0')
    
    with open('./config.cfg', 'w') as file:
        config.write(file)
    
    file.close()    
    return
    
def configura():
#configura il file di configurazione.
    
    config = ConfigParser.RawConfigParser()
    config.read('./config.cfg')
    consumer_token = config.get( 'applicazione', 'consumer_token')
    
    if consumer_token == '0':
        consumer_token = raw_input('ERRORE: Consumer token assente.\n Inserire consumer token:')
        config.set('applicazione', 'consumer_token', consumer_token)
    
    consumer_secret = config.get( 'applicazione', 'consumer_secret')

    if consumer_secret == '0':
        consumer_secret = raw_input('ERRORE: Consumer secret assente.\n Inserire consumer secret:')
        config.set('applicazione', 'consumer_secret', consumer_secret)

# inizio la procedura di autenticazione con OAuthHandler, fornendogli le nostre chiavi d'accesso.

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    
# adesso tocca all'utente: devo fargli aprire una finestra del browser 
# sull'url per l'autenticazione fornito da twitter, una volta che ha autorizzato la 
# nostra app l'utente riceve un codice che poi deve darci piu' avanti.
    
    try:
        redirect_url = auth.get_authorization_url()	#salvo l'url generato per l'autenticazione
        webbrowser.open( redirect_url)			#faccio aprire quell'url al browser.
    except tweepy.TweepError:
        print 'ERRORE! Richiesta di autenticazione fallita.'    
        exit()
        
    verifier = raw_input('Codice:')			#tipo scanf. Visualizza il parametro e aspetta un input dall'utente.
    
    try:
        auth.get_access_token(verifier)			#chiedo di prendere le chiavi d'accesso abbinate all'utente che ci ha dato il codice.
    except tweepy.TweepError:
        print 'ERRORE! Autenticazione fallita.'
        exit()
    
    user_key = auth.access_token.key
    user_secret = auth.access_token.secret
    utente = auth.get_username()
    config.set('utente', 'key', user_key)
    config.set('utente', 'secret', user_secret)
    config.set('utente', 'nome_utente', utente)
    
    with open('./config.cfg', 'w') as file:
        config.write(file)
    
    file.close()
    return    

def autenticazione ():
#funzione che gestisce la configurazione per l'accesso alle API twitter. restituisce una "chiave" per aprire le API

# fatto tutto! Adesso carichiamo in bot le api, fornendo auth che ora contiene 
# sia le nostre chiavi, sia quelle dell'utente.
    config = ConfigParser.RawConfigParser()
    config.read('./config.cfg')
    consumer_secret = config.get('applicazione', 'consumer_secret')
    consumer_key = config.get ('applicazione', 'consumer_token')
    key = config.get('utente', 'key')
    secret = config.get('utente', 'secret')
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return (auth)
    
def parametri_avvio():
#funzione che gestisce i parametri passati all'avvio

    opzioni = argparse.ArgumentParser()
    opzioni.add_argument('--registra', '-r', help='registra un nuovo utente', action='store_true')
    opzioni.add_argument('--nuovotweet', '-nt', help='aggiungi un tweet all\'elenco', action='store_true')
    argomenti = opzioni.parse_args()
    return argomenti
    

def time_division(t_up):
#ritorna un oggetto formato t_data formato dai campi
#days hours minutes e seconds. essi contengono la suddivisione
#del tempo t_up passato come parametro(espresso in secondi).
  
    temp = t_date()
    temp.seconds=t_up%60 
    t_up=t_up/60
    temp.minutes=t_up%60
    t_up=t_up/60
    temp.hours=t_up%24
    temp.days=t_up/24
    return temp

def time_up(t_start):
#restituisce un oggetto tipo t_data con i suoi campi(vedi commento
#del sottoprogramma time_division per i campi) completati.
 
    t_end = time.time()
    t_up = t_end - t_start
    tempo = time_division(t_up)
    return tempo


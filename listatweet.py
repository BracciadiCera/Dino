import ConfigParser

# crea il file che contiene l'elenco dei tweet
def creaLista():
        
    file = open('./tweet.cfg', 'w')
    file.close()
    
    return

def aggiungitweet():
    
    tweet = ConfigParser.RawConfigParser()
    tweet.read('./tweet.cfg')
    sezioni = tweet.sections()
    print 'LE SEZIONI DISPONIBILI SONO:'
    print sezioni
    ok = False
    while ok != True:
        sezione_tweet = raw_input('In quale sezione inserire?\n')
        if tweet.has_section(sezione_tweet)==True: 
            ok = True
        else:
            print 'SEZIONE INESISTENTE'
    
    allocati = tweet.getint(sezione_tweet, 'allocati')
    disponibili = 140 - allocati
    ok = False
    while ok != True:
        testo = raw_input('Inserire testo tweet:\n' + str(disponibili) + ' caratteri disponibili\n')
        if len(testo) <= disponibili:
            ok = True
        else:
            print '\n troppo lungo, taglia! (hai sforato di: ' + str(len(testo)-disponibili) + ' caratteri)\n'
    
    esistenti = len( tweet.options(sezione_tweet) ) - 1  #per ora c'e' il campo 'allocati', poi dovrebbe essere spostato.
    numero_nuovo = str( esistenti + 1 )
    tweet.set(sezione_tweet, numero_nuovo, testo)

    with open('./tweet.cfg', 'w') as file_tweet:
        tweet.write(file_tweet)
    
    file_tweet.close()
    return
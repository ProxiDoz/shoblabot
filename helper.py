import json, time
from random import randint, seed

__faggots = []
__enable_log = True

def __faggotLog( text ):
    global __enable_log

    if not __enable_log:
        return

    print( '[helper: {}]: > {}'.format( time.strftime("%H:%M:%S"), text ) )

def __loadFaggotsEUCountries():
    __faggotLog('load __faggots EU country list to the RAM...')
    global __faggots

    try:
        f = open('__faggots.json')
        __faggots = json.load(f)
        f.close()
    except Exception as e:
        __faggotLog('error: {}'.format(e))
        return False

    __faggotLog('done.')
    return True

def __getRandomFaggotEUCountry():
    __faggotLog('get random faggot EU country from list...')
    global __faggots
    
    fagg = {}
    try:
        seed( time.time() )
        index = randint( 0, len(__faggots) - 1 )
        fagg = __faggots[ index ]
    except Exception as e:
        __faggotLog('error: {}'.format(e))

    __faggotLog('done.')
    return fagg

def setFaggotLog( flag = True ):
    global __enable_log
    __enable_log = flag

def getFaggotEUCountryRequest( message_text = '', request_string_list = [] ):
    __faggotLog('get random faggot EU country if requested string exists in the message...')

    if not message_text:
        __faggotLog('error: message_text is null')

    if not request_string_list:
        __faggotLog('error: request_string is null')

    pure_text = message_text.replace(' ', '').lower().replace('ё', 'е')

    for req in request_string_list:
        req = req.lower()
        if pure_text.find( req ) != -1:
            fag = __getRandomFaggotEUCountry()
            if fag:
                return ( True, fag )
            else:
                return ( False, {} )

setFaggotLog()
__loadFaggotsEUCountries()

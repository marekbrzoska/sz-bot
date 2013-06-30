#-*- coding=utf-8 -*- 

def createMessage(lecture):
    '''Generate message to be given to a subscribed user.'''
    return u'''Witaj!\n\n

    Na przedmiocie https://zapisy.ii.uni.wroc.pl/s/opis.php3?id=%d pojawiło się wolne miejsce. Jeżeli podałeś swój login i hasło, zapisobot spróbował Cię tam zapisać. Sprawdź swój plan.
    ''' % lecture

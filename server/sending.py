#-*- coding: utf-8 -*-

from smtplib import SMTP
import xmpp

__xmpp_connection = None

def __connect():
    '''
Description:
    Connect to jabber and store the connection in modules privat variable.

Return value:
    xmpp.Client, connected and authetified
    '''

    global __xmpp_connection
    c = xmpp.Client('gmail.com')
    c.connect(server=('talk.google.com',5223))
    c.auth('zapisobot','treflutreflu')
    __xmpp_connection = c
    return c

def send_xmpp(recipient, msg):
    '''
Description:
    Send msg to recipient. Connect first, if necessary.
    xmpp account is zapisobot@gmail.com
    '''
    global __xmpp_connection
   
    try:
        if not __xmpp_connection:
            __xmpp_connection = __connect()
        __xmpp_connection.send(xmpp.Message(recipient,msg))
        print 'xmpp sent to:', recipient
    except Exception, e:
        send_email('brzoskamarek@gmail.com','Kurde, wiadmości xmpp znowu nie chcą działać...')





def send_email(recipient, msg):
    '''
Description:
    Send e-mail message msg to recipient. 
    msg need not to be unicode and need to contain only message body, all
    headers are added automatically.
    Message will be signed by Zapisobot, and sent from zapisobot@prokonto.pl.    
    receipient need to have format: \"person@server\""
    '''
    server = 'poczta.o2.pl'
    username = 'zapisobot'
    password = 'pinw0'
    

    try:
        server = SMTP(server)
        try:
            server.login(username, password)
        except Exception:
            raise Exception, "Could not login as %s" % username
    except Exception, e:
        print "Could not connect SMTP server %s" % server
        

    message = 'From: Zapisobot II<zapisobot@prokonto.pl>\n'\
                'Subject:Powiadomienie\n\n\n'\
                + msg +\
                '\n\n  pozdrawiam,\n'\
                '  Zapisobot.'
    #print message
     
    try:
        server.sendmail('zapisobot@tlen.pl',recipient,message)
        print 'email sent to:', recipient
    except Exception:
        try:
            print "nie wysłałem do %s" % recipient
        except Exception:
            try:
                print "nie wysłałem do:"
                print recipient.__str__()
            except Exception:
                print "Cholera, nie wiem do kogo nie wysłałem..."
        #raise Exception, "Couldn't send message to %s" % recipient
    


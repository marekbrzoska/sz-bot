#-*- coding=utf-8 -*-
from sending import send_email, send_xmpp
from login import check, subscribe
from message import createMessage
from pysqlite2 import dbapi2 as sqlite
from time import sleep
from unicodedata import normalize as normal

def process(row):
    '''
Description:
    Do all the work assigned to a single record in waiting queue, e.g.:
        check for available places
        if any send email/send jabber message/subscribe 

Return value:
    record's id (integer) if there are any available places, None otherwise

Arguments:
    tuple containing single record of a task
    '''
    (id, lecture, groupType, group, groupInternal, login, passwd, email, jabber) = row
    availableSlots = check(lecture, groupType, group)
    if availableSlots:
        try:
            msg = createMessage(lecture)
            send_email(email, normal('NFKD',msg).encode('latin2','ignore'))
            if jabber: send_xmpp(jabber, msg)
            if login:
                subscribe(login, passwd, lecture, groupInternal)
        except Exception:
            pass
        return id
    return None

def loop():
    '''
Description:
    Infinitely loop over the waiting list. If any record finds a free place,
    delete it from database, and notify/subscribe it's user.

    After every iteration sleep for 60 seconds.
    
    
    '''
    conn = sqlite.connect('../../baza')
    c = conn.cursor()
    e = c.execute

    while True:
        e('SELECT * FROM gui_task ORDER BY id')
        rowlist = c.fetchall()
        dellist = []
        for row in rowlist:
            effect = process(row)
            if effect: dellist.append(effect)
        for id in dellist:
            e('DELETE FROM gui_task WHERE id=%d' % id)
        conn.commit()
        sleep(60)

if __name__ == "__main__":
    loop()


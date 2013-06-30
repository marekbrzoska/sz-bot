#-*- coding: utf-8 -*-

try:
    import mechanize
    import cookielib
    import re
    from BeautifulSoup import BeautifulSoup
    from sending import send_xmpp
except Exception:
    raise Exception, 'One or more imports failed.'



def check(lectureId, groupType, groupNumber):
    '''
Description:
    This function checks particular group for available places. 

Return value:
    number of available places

Arguments:

    lectureId:
    integer or string representation of integer

    groupType: can have one of 3 possible values: 
    'c' 
    'p' 
    'cp'
    's'.

    groupNumber:
    integer or string representation of integer
    simply number of the group you check. It's at the begining of the row of interest.
    '''

    lectureId = int(lectureId)
    groupNumber = int(groupNumber)
    if groupType == 'c':
        groupType = u'Ćwiczenia:'
    elif groupType == 'p':
        groupType = u'Pracownie:'
    elif groupType == 'cp':
        groupType = u'Ćwiczenia+pracownie:'
    elif groupType == 's':
        groupType = u'Grupy seminaryjne:'
    else:
        print 'Błędzik: Nie ma takiego rodzaju zajec pomocniczych.'
        print lectureId, groupType, groupNumber
        return 999

    url = 'https://zapisy.ii.uni.wroc.pl/s/opis.php3?id=%d' % lectureId

    br = __login('gosc','')
    # Otwieramy stronę jakiegoś przedmiotu
    br.open(url)

    # Wczytujemy zawartość strony
    html = br.response().read()

    # Wrzucamy stronę do garnka i robimy z niej zupkę:)
    soup = BeautifulSoup(html)

    try:
        o = soup.find(text=groupType)

        row = o.parent.parent.parent.parent.nextSibling.find(text=(u'%d.' % groupNumber)).parent.parent # daje nam wiersz grupy do której chcemy się zapisać
        row = filter(lambda x: x != '\n', row)                                                          # pozbywamy sie tych beznadziejnych pól
        pair = row[3:5]                                                                                 # dwa interesujące nas pola
        mx = int(re.search(r'[0-9]+', pair[0].contents[0]).group())                                     # wyciągamy limit grupy
        cr = int(re.search(r'[0-9]+', pair[1].contents[0]).group())                                     # wyciągamy stan grupy
        return mx - cr # max
    except Exception:
        print "Oooops, błędzik!"
        print "Probable cause: incorrect group or something like that."
        try:
            send_xmpp('brzoza@jabster.pl','coś się sypnęło. Po szczegóły zapraszam do logów:) Wyszukaj sobie linijkę ze słowem: błędzik;)')
            print "id:"
            print lectureId
            print "type:"
            print groupType
            print "group:"
            print groupNumber
            return 99999
        except Exception:
            print "Fatal exception in check. Let's delete the cause."
            return 99999



def __login(username, password):
    '''
Description:
    Function logins to zapisy.ii.uni.wroc.pl with given username and password.
    
Return value:
    mechanize.Browser object with established connection

Arguments:

    username:
    string

    password:
    string
    '''
    br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # The site we will navigate into, handling it's session
    br.open('https://zapisy.ii.uni.wroc.pl/s/login.php3')
    # Select the first (index zero) form
    br.select_form(nr=0)

    # User credentials
    br.form['username'] = username
    br.form['password'] = password

    # Login
    br.submit()

    return br


def subscribe(user, passwd, lecture,group):
    user = str(user)
    group = str(group)
    url = 'https://zapisy.ii.uni.wroc.pl/s/opis.php3?id=%d' % lecture

    br = __login(user,passwd)
    # Otwieramy stronę jakiegoś przedmiotu
    br.open(url)

    # Wczytujemy zawartość strony
    html = br.response().read()
    # gotujemy zupkę
    soup = BeautifulSoup(html)
    # znajdujemy wszystkie guziki zapisz/przenieś
    zapisze = soup.findAll(attrs={'value':re.compile(u'Zapisz/Przenieś')})
    # sprawdzamy przy którym guziku występuje nasza grupa
    for x in xrange(len(zapisze)):
        if zapisze[x].parent.previousSibling.previousSibling.find(attrs={'value' : group}): number = x
    br.select_form(nr=number)
    br.form.controls[0].set(True, group)
    br.submit()
    br.open('https://zapisy.ii.uni.wroc.pl/s/logout.php3')




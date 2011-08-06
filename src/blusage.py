import datetime

from BeautifulSoup import BeautifulSoup

class DailyUsage(object):
    def __init__(self, day="", dataUsed=0, detail=[]):
        self.day = day
        self.dataUsed = dataUsed
        self.detail = detail

class BLUsage(object):
    name = ""
    username = ""
    password = ""

    last_update = ""

    usage = []
    totalKB = 0
    capKB = 0

    @property
    def error(self):
        return self._error
    _error = ""

    def __init__(self):
        today = datetime.date.today()
        self.start = datetime.date(year=today.year, month=today.month, day=1)
        self.end = self.start + datetime.timedelta(days=29)

    def parse(self, html):
        html = html.lower()

        try:
            # attempt to sanitize teh html
            html = html.replace('&nbsp;', '')
            html = html.replace('style=&{head};', '')
            e = [('<head', '</head>'), ('<script', '</script>'),
                 ('<!--', '-->')]
            for elem in e:
                while True:
                    begin = html.find(elem[0])
                    if begin < 0:
                        break
                    end = html.find(elem[1])
                    html = html[:begin] + html[end + len(elem[1]):]

            begin = html.find('<body')
            end = html.find('>', begin)
            html = html[:begin + 5] + html[end:]

            soup = BeautifulSoup(unicode(html),
                                 convertEntities=BeautifulSoup.HTML_ENTITIES)
            rows  = soup.findAll('table')[14]('tr')

            self.usage = []
            date = None
            timely = []
            dataKB = 0
            self.totalKB = 0
            for row in rows[1:-1]:
                tds = [td.font.contents[0] for td in row('td')[2:]]
                if not date == tds[0]:
                    if date:
                        self.totalKB += dataKB
                        self.usage.append(DailyUsage(date, dataKB, timely))
                    date = tds[0]
                    dataKB = 0
                    timely = []
                dataKB += int(tds[2])
                timely.append(tds[1:])
            if date:
                self.totalKB += dataKB
                self.usage.append(DailyUsage(date, dataKB, timely))
        except:
            self._error = 'Could not get data.'
            return False

        self.last_update = datetime.datetime.now()
        return True

    def remaining(self):
        if not self.capKB:
            return "Unlimited"
        if not self.totalKB:
            return self.capKB
        return self.capKB - self.totalKB

    def smart_bytes(self, data):
        if data < 1500:
            return '%d KB' % data
        elif data < 1500000:
            return '%.2f MB' % (data / 1024.)
        else:
            return '%.2f GB' % (data / (1024. * 1024.))


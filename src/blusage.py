import urllib
import json
import os
import logging

from PySide.QtCore import QDate

from BeautifulSoup import BeautifulSoup

USAGE_FILE_PATH = os.path.expanduser('~/.blusage/usage.json')
logger = logging.getLogger('BLUsage')

class DailyUsage(object):
    def __init__(self, day="", dataUsed=0, detail=[]):
        self.day = day
        self.dataUsed = dataUsed
        self.detail = detail

    def to_dict(self):
        return {
            'day': self.day,
            'data': self.dataUsed,
            'detail': [dict(time=d[0], data=d[1]) for d in self.detail],
        }


class BLUsage(object):
    name = ""
    username = ""
    password = ""

    last_update = None

    usage = []
    totalKB = 0
    capKB = 0

    def __init__(self):
        today = QDate.currentDate()
        self.start = QDate(today.year(), today.month(), 1)
        self.end = self.start.addDays(29)
        try:
            with file(USAGE_FILE_PATH, 'r') as f:
                self.json_to_usage(f.read())
        except Exception as e:
            logger.debug(e)

    @property
    def error(self):
        return self._error
    _error = ""

    @property
    def user_endpoint(self):
        return "https://%s:%s@care.banglalionwimax.com/User" % (self.username,
                                                                self.password)

    @property
    def post_data(self):
        return urllib.urlencode({
            'Page': 'UsrSesHit',
            'Title': 'Session Calls',
            'UserID': self.username,
            'StartDate': self.start.toString("dd/MM/yyyy"),
            'EndDate': self.end.toString("dd/MM/yyyy"),
            'Submit': 'Submit',
        })

    def usage_to_json(self):
        usage = []
        for u in self.usage:
            usage.append(u.to_dict())
        return json.dumps(usage)

    def json_to_usage(self, d):
        usage = json.loads(d)
        self.usage = []
        for u in usage:
            daily = DailyUsage(u['day'], u['data'])
            daily.detail = [[d['time'], d['data']] for d in u['detail']]
            self.usage.append(daily)

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
            with file(USAGE_FILE_PATH, 'w') as f:
                f.write(self.usage_to_json())
        except Exception as e:
            logger.debug(e)
            self._error = 'Could not get data.'
            return False

        self.last_update = QDate.currentDate()
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


import os
import csv
import urllib

from PySide.QtCore import Qt, QAbstractTableModel
from BeautifulSoup import BeautifulSoup

INVOICE_CSV = os.path.expanduser('~/.blusage/invoices.csv')

class Invoice(QAbstractTableModel):

    def __init__(self, parent=None):
        super(Invoice, self).__init__(parent)
        try:
            os.mkdir(os.path.expanduser('~/.blusage'))
        except Exception as e:
            print e
        self.invoices = []
        try:
            with open(INVOICE_CSV, 'r') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    self.invoices.append(row)
        except Exception as e:
            print e

        self.header = ['Record', 'Date', 'Credit', 'Debit', 'Balance']

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]
            else:
                return section + 1

    def rowCount(self, parent):
        return len(self.invoices)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.invoices[index.row()][index.column()+1]

    @property
    def post_data(self):
        return urllib.urlencode({
            'Page': 'BillTransHit',
            'Title': 'Transaction History',
        })

    def parse(self, html):
        try:
            # attempt to sanitize teh html
            html = html.replace('&nbsp;', '')
            html = html.replace('STYLE=&{head};', '')
            begin = html.find('<BODY')
            end = html.find('>', begin)
            html = html[:begin + 5] + html[end:]

            soup = BeautifulSoup(unicode(html))
            rows = soup.findAll('table')[14]('tr')
            self.invoices = []
            for row in rows[1:]:
                tds = row('td')
                csvrow = [tds[0].font.a['href'],]
                for td in tds:
                    csvrow.append(td.find(text=True) or '')
                csvrow[1] = csvrow[1].replace(' # ', '-')
                self.invoices.append(csvrow)

            with open(INVOICE_CSV, 'w') as f:
                csvwriter = csv.writer(f)
                for row in self.invoices:
                    csvwriter.writerow(row)
        except Exception as e:
            print e
            self._error = 'Could not get data.'
            return False

        except Exception as e:
            print e

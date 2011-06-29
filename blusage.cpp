#include "blusage.h"

#include <QDomDocument>
#include <tidy/tidy.h>
#include <tidy/buffio.h>

BLUsage::BLUsage(){
    QDate today = QDate::currentDate();
    start = QDate(today.year(), today.month(), 1);
    end = start.addDays(29);
}

QString BLUsage::errorString() {
    return error;
}

bool BLUsage::parse(QString html) {
    // tidy the horrible html
    html = tidy(qPrintable(html));

    if (html.isEmpty()) {
        error = "Malformed HTML. Could not tidy it.";
        return false;
    }
    // remove all unwanted/invalid elements
    html = html.toLower();
    html.replace("&nbsp;", "");

    QList<QStringList> elems;
    elems.append(QStringList() << "<head" << "</head>");
    elems.append(QStringList() << "<script" << "</script>");
    elems.append(QStringList() << "<!--" << "-->");

    int left, right;
    QStringList l;
    foreach (l, elems) {
        forever {
            left = html.indexOf(l[0]);
            right = html.indexOf(l[1]);
            if (left == -1)
                break;
            html = html.left(left) + html.right(html.size() - right - l[1].size());
        }
    }

    left = html.indexOf("<body");
    right = html.indexOf(">", left);
    html = html.left(left + 5) + html.right(html.size() - right);

    QDomDocument doc("blusage");
    if (!doc.setContent(html)) {
        error = "Could not parse it!!";
        return false;
    }

    QDomNodeList rows = doc.documentElement().elementsByTagName("table").at(14).childNodes();
    if (rows.isEmpty()) {
        error = "Could not find data.";
        return false;
    }

    usage.clear();
    for (int i=1; i<rows.size()-1; i++) {
        QDomNodeList tds = rows.at(i).childNodes();
        QStringList l;
        for (int j=2; j<5; j++) {
            l << tds.at(2).firstChildElement().text();
        }
        usage.append(l);
    }

    return true;
}

QString BLUsage::tidy(const char* input) {
    TidyBuffer output = {0};
    TidyBuffer errbuf = {0};
    int rc = -1;
    Bool ok;

    TidyDoc tdoc = tidyCreate();                     // Initialize "document"

    ok = tidyOptSetBool( tdoc, TidyXhtmlOut, yes );  // Convert to XHTML
    if ( ok )
      rc = tidySetErrorBuffer( tdoc, &errbuf );      // Capture diagnostics
    if ( rc >= 0 )
      rc = tidyParseString( tdoc, input );           // Parse the input
    if ( rc >= 0 )
      rc = tidyCleanAndRepair( tdoc );               // Tidy it up!
    if ( rc >= 0 )
      rc = tidyRunDiagnostics( tdoc );               // Kvetch
    if ( rc > 1 )                                    // If error, force output.
      rc = ( tidyOptSetBool(tdoc, TidyForceOutput, yes) ? rc : -1 );
    if ( rc >= 0 )
      rc = tidySaveBuffer( tdoc, &output );          // Pretty Print

    QString html = (rc >= 0) ? QString((const char*)output.bp) : "";

    tidyBufFree( &output );
    tidyBufFree( &errbuf );
    tidyRelease( tdoc );

    return html;
}

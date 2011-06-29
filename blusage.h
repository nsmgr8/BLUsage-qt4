#ifndef BLUSAGE_H
#define BLUSAGE_H

#include <QtCore>

class BLUsage
{
public:
    BLUsage();

    bool parse(QString html);

    QString name;
    QString username;
    QString password;

    QDate start;
    QDate end;

    QList<QStringList> usage;

    QString errorString();

private:
    QString tidy(const char* html);

    QString error;
};

#endif // BLUSAGE_H

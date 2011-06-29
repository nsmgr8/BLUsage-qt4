#ifndef BLUSAGE_H
#define BLUSAGE_H

#include <QtCore>

class BLUsage
{
public:
    BLUsage();

    QString name;
    QString username;
    QString password;

    QDate start;
    QDate end;
};

#endif // BLUSAGE_H

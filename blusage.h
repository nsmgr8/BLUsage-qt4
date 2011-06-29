#ifndef BLUSAGE_H
#define BLUSAGE_H

#include <QtCore>

struct DailyUsage {
    QString day;
    int dataUsed;
    QList<QStringList> detail;
};

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
    QDateTime lastUpdate;

    QList<DailyUsage> usage;
    int totalKB;

    QString errorString();

private:
    QString tidy(const char* html);

    QString error;
};

#endif // BLUSAGE_H

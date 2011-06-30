#ifndef BLUSAGE_H
#define BLUSAGE_H

#include <QtCore>

struct DailyUsage {
    QString day;
    quint32 dataUsed;
    QList<QStringList> detail;
};

QDataStream &operator<<(QDataStream &out, const DailyUsage &daily);
QDataStream &operator>>(QDataStream &in, DailyUsage &daily);

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
    quint32 totalKB;
    quint32 capKB;

    QString errorString();
    QString smartBytes(int kb);

private:
    QString tidy(const char* html);

    QString error;
};

QDataStream &operator<<(QDataStream &out, const BLUsage &usage);
QDataStream &operator>>(QDataStream &in, BLUsage &usage);

#endif // BLUSAGE_H

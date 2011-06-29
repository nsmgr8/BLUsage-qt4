#include "blusage.h"

BLUsage::BLUsage(){
    QDate today = QDate::currentDate();
    start = QDate(today.year(), today.month(), 1);
    end = start.addDays(29);
}

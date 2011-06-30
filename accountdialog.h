#ifndef ACCOUNTDIALOG_H
#define ACCOUNTDIALOG_H

#include <QDialog>

#include "blusage.h"

namespace Ui {
    class AccountDialog;
}

class AccountDialog : public QDialog
{
    Q_OBJECT

public:
    AccountDialog(blusage::BLUsage *model, QWidget *parent = 0);
    ~AccountDialog();

    void accept();
private:
    Ui::AccountDialog *ui;
    blusage::BLUsage *model;
};

#endif // ACCOUNTDIALOG_H

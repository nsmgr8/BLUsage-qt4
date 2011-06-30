#include "accountdialog.h"
#include "ui_accountdialog.h"

AccountDialog::AccountDialog(blusage::BLUsage *model, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AccountDialog)
{
    ui->setupUi(this);

    ui->capEdit->setValidator(new QIntValidator(0, 100000000, this));

    ui->accountNameEdit->setText(model->name);
    ui->usernameEdit->setText(model->username);
    ui->passwordEdit->setText(model->password);

    ui->capEdit->setText(QString("%1").arg(model->capKB));
    ui->fromDate->setDate(model->start);
    ui->toDate->setDate(model->end);

    this->model = model;
}

AccountDialog::~AccountDialog()
{
    delete ui;
}

void AccountDialog::accept() {
    model->name = ui->accountNameEdit->text();
    model->username = ui->usernameEdit->text();
    model->password = ui->passwordEdit->text();

    model->capKB = ui->capEdit->text().toInt();
    model->start = ui->fromDate->date();
    model->end = ui->toDate->date();

    QDialog::accept();
}

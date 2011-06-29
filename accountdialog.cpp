#include "accountdialog.h"
#include "ui_accountdialog.h"

AccountDialog::AccountDialog(BLUsage *model, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AccountDialog)
{
    ui->setupUi(this);

    ui->accountNameEdit->setText(model->name);
    ui->usernameEdit->setText(model->username);
    ui->passwordEdit->setText(model->password);
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
    model->start = ui->fromDate->date();
    model->end = ui->toDate->date();

    QDialog::accept();
}

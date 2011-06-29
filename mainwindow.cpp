#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "blusage.h"
#include "accountdialog.h"

#include <qnetworkrequest.h>
#include <qnetworkreply.h>
#include <qmessagebox.h>

#include "treemodel.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QMenu *menu = new QMenu(QString("File"), this);
    menu->addAction(ui->actionAccount);
    menu->addAction(ui->actionUpdate);
    menu->addSeparator();
    menu->addAction(ui->actionQuit);

    ui->menuBar->addMenu(menu);

    this->connect(ui->actionAccount, SIGNAL(triggered()), SLOT(showAccountEditor()));
    this->connect(ui->actionUpdate, SIGNAL(triggered()), SLOT(updateUsage()));

    networkAccessManager = new QNetworkAccessManager;
    this->connect(networkAccessManager, SIGNAL(finished(QNetworkReply*)), SLOT(fetchedUsages(QNetworkReply*)));
    this->connect(networkAccessManager, SIGNAL(sslErrors(QNetworkReply*,QList<QSslError>)), SLOT(allowConnection(QNetworkReply*)));

    TreeModel *model = new TreeModel("Col11\tCol12\n Col21\tCol22\n  Col31\tCol32", this);
    ui->treeView->setModel(model);

    if (usageModel.username.isEmpty()) {
        showAccountEditor();
    }

    ui->accountName->setText(usageModel.name);
}

MainWindow::~MainWindow()
{
    delete networkAccessManager;
    delete ui;
}

void MainWindow::showAccountEditor() {
    AccountDialog(&usageModel, this).exec();
    ui->accountName->setText(usageModel.name);
}

void MainWindow::updateUsage() {
    QUrl url = QUrl(QString("https://care.banglalionwimax.com/User"));
    QString auth = QString("%1:%2").arg(usageModel.username).arg(usageModel.password);

    QNetworkRequest request = QNetworkRequest(url);
    request.setRawHeader("Authorization", QString("Basic " + QByteArray(auth.toLocal8Bit().toBase64())).toLocal8Bit());

    QByteArray postData;
    postData.append("Page=UsrSesHit&");
    postData.append("Title=Session Calls&");
    postData.append(QString("UserID=%1&").arg(usageModel.username));
    postData.append(QString("StartDate=%1&").arg(usageModel.start.toString("dd/MM/yyyy")));
    postData.append(QString("EndDate=%1&").arg(usageModel.end.toString("dd/MM/yyyy")));
    postData.append("Submit=Submit");

    networkAccessManager->post(request, postData);
    ui->updateButton->setEnabled(false);
}

void MainWindow::fetchedUsages(QNetworkReply *reply) {
    ui->updateButton->setEnabled(true);

    QString title;
    QString message;

    switch(reply->error()) {
    case QNetworkReply::AuthenticationRequiredError:
    case QNetworkReply::ContentAccessDenied:
        title = QString("Authentication Error");
        message = QString("Please check your account credentials.");
        break;
    case QNetworkReply::NoError:
        if (!usageModel.parse(QString(reply->readAll()))) {
            title = "Parsing error";
            message = usageModel.errorString();
        }
        return;
    default:
        title = QString("An error occured");
        message = reply->errorString().append(".\nPlease check your internet connection.");
    }

    QMessageBox::critical(this, title, message, QString("OK"));
}

void MainWindow::allowConnection(QNetworkReply *reply) {
    reply->ignoreSslErrors();
}

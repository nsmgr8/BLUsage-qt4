#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <qnetworkrequest.h>
#include <qnetworkreply.h>
#include <qmessagebox.h>

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
}

MainWindow::~MainWindow()
{
    delete networkAccessManager;
    delete ui;
}

void MainWindow::showAccountEditor() {
    qDebug("Open the account editor");
}

void MainWindow::updateUsage() {
    QUrl url = QUrl(QString("https://care.banglalionwimax.com/User"));
    QString username = "abcd.1234";
    QString password = "123456";
    QByteArray auth = QString("").append(username).append(":").append(password).toLocal8Bit();

    QNetworkRequest request = QNetworkRequest(url);
    request.setRawHeader("Authorization", QString("Basic " + QByteArray(auth.toBase64())).toLocal8Bit());

    QByteArray postData;
    postData.append("Page=UsrSesHit&");
    postData.append("Title=Session Calls&");
    postData.append(QString("UserID=").append(username).append("&"));
    postData.append("StartDate=03/06/2011&");
    postData.append("EndDate=02/07/2011&");
    postData.append("Submit=Submit");

    networkAccessManager->post(request, postData);
}

void MainWindow::fetchedUsages(QNetworkReply *reply) {
    QString title;
    QString message;

    switch(reply->error()) {
    case QNetworkReply::AuthenticationRequiredError:
    case QNetworkReply::ContentAccessDenied:
        title = QString("Authentication Error");
        message = QString("Please check your account credentials.");
        break;
    case QNetworkReply::NoError:
        qDebug(reply->readAll());
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

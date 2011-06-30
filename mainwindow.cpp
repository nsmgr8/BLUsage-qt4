#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "blusage.h"
#include "accountdialog.h"

#include <qnetworkrequest.h>
#include <qnetworkreply.h>
#include <qmessagebox.h>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->setWindowIcon(QIcon(":/blusage.png"));

    QMenu *menuFile = new QMenu(QString("File"), this);
    menuFile->addAction(ui->actionAccount);
    menuFile->addAction(ui->actionUpdate);
    menuFile->addSeparator();
    menuFile->addAction(ui->actionQuit);

    QMenu *menuHelp = new QMenu("Help", this);
    menuHelp->addAction(ui->actionAbout);

    ui->menuBar->addMenu(menuFile);
    ui->menuBar->addMenu(menuHelp);

    this->connect(ui->actionAccount, SIGNAL(triggered()), SLOT(showAccountEditor()));
    this->connect(ui->actionUpdate, SIGNAL(triggered()), SLOT(updateUsage()));
    this->connect(ui->actionAbout, SIGNAL(triggered()), SLOT(about()));

    networkAccessManager = new QNetworkAccessManager;
    this->connect(networkAccessManager, SIGNAL(finished(QNetworkReply*)), SLOT(fetchedUsages(QNetworkReply*)));
    this->connect(networkAccessManager, SIGNAL(sslErrors(QNetworkReply*,QList<QSslError>)), SLOT(allowConnection(QNetworkReply*)));

    fileName = QDir::homePath().append("/.BLUsage.dat");
    readUsage();

    treeModel = new TreeModel(usageModel.usage);
    ui->treeView->setModel(treeModel);
    ui->treeView->resizeColumnToContents(0);

    if (usageModel.username.isEmpty()) {
        showAccountEditor();
    }

    ui->treeView->setAlternatingRowColors(true);
    ui->accountName->setText(usageModel.name);
    ui->progressBar->setHidden(true);
    showLastUpdate();
}

MainWindow::~MainWindow()
{
    delete treeModel;
    delete networkAccessManager;
    delete ui;
}

void MainWindow::about() {
    QMessageBox::about(this, "BLUsage", "Bangla Lion bandwidth usage viewer.\n\n\tVersion 1.0\n\nAuthor: M. Nasimul Haque\n\nemail: nasim.haque@gmail.com\n\nweb: http://www.nasim.me.uk");
}

void MainWindow::showAccountEditor() {
    AccountDialog(&usageModel, this).exec();
    ui->accountName->setText(usageModel.name);
    writeUsage();
    showLastUpdate();
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

    QNetworkReply *reply = networkAccessManager->post(request, postData);
    this->connect(reply, SIGNAL(downloadProgress(qint64,qint64)), SLOT(showProgress(qint64,qint64)));

    ui->updateButton->setEnabled(false);
    ui->progressBar->setHidden(false);
    ui->progressBar->setValue(0);
    ui->statusBar->showMessage("Please wait...");
}

void MainWindow::fetchedUsages(QNetworkReply *reply) {
    ui->updateButton->setEnabled(true);
    ui->progressBar->setHidden(true);
    reply->disconnect(this, SLOT(showProgress(qint64,qint64)));

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
        else {
            treeModel->deleteLater();
            treeModel = new TreeModel(usageModel.usage);
            ui->treeView->setModel(treeModel);
            ui->treeView->resizeColumnToContents(0);
            showLastUpdate();
            writeUsage();
        }
        return;
    default:
        title = QString("An error occured");
        message = reply->errorString().append(".\nPlease check your internet connection.");
    }

    QMessageBox::critical(this, title, message, QString("OK"));
    reply->deleteLater();
}

void MainWindow::allowConnection(QNetworkReply *reply) {
    reply->ignoreSslErrors();
}

void MainWindow::showProgress(qint64 received, qint64 total) {
    if (total <= 0)
        total = 100000;
    ui->progressBar->setValue(float(received)/float(total)*100.);
}

void MainWindow::showLastUpdate() {
    if (usageModel.lastUpdate.isNull()) {
        ui->statusBar->showMessage("Ready");
    }
    else {
        ui->totalLabel->setText(QString("Totals usage: <b>%1</b>").arg(usageModel.smartBytes(usageModel.totalKB)));
        if (usageModel.capKB > 0) {
            ui->remainingLabel->setText(QString("Remaining: <b>%1</b>").arg(usageModel.smartBytes(usageModel.capKB - usageModel.totalKB)));
        }
        else {
            ui->remainingLabel->setText("Remaining: <b>Unlimited</b>");
        }
        ui->statusBar->showMessage(usageModel.lastUpdate.toString("dd MMM, yyyy HH:mm").prepend("Last updated on: "));
    }
}

void MainWindow::readUsage() {
    QFile file(fileName);
    if(!file.open(QIODevice::ReadOnly))
        return;
    QDataStream in(&file);
    in >> usageModel;
    file.close();
}

void MainWindow::writeUsage() {
    QFile file(fileName);
    if(!file.open(QIODevice::WriteOnly))
        return;
    QDataStream out(&file);
    out << usageModel;
    file.close();
}

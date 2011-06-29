#include "mainwindow.h"
#include "ui_mainwindow.h"

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
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::showAccountEditor() {
    qDebug("Open the account editor");
}

void MainWindow::updateUsage() {
    qDebug("Update usage");
}

#include "mainwindow.h"
#include "ui_mainwindow.h"

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

    TreeModel *model = new TreeModel("Col11\tCol12\n Col21\tCol22\n  Col31\tCol32", this);
    ui->treeView->setModel(model);
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

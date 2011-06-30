#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <qnetworkaccessmanager.h>

#include "blusage.h"
#include "treemodel.h"

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

protected slots:
    void showAccountEditor();
    void updateUsage();
    void fetchedUsages(QNetworkReply *reply);
    void allowConnection(QNetworkReply *reply);

    void about();

private:
    Ui::MainWindow *ui;
    QNetworkAccessManager *networkAccessManager;

    blusage::BLUsage usageModel;
    TreeModel *treeModel;

    QString fileName;

    void showLastUpdate();
    void readUsage();
    void writeUsage();
};

#endif // MAINWINDOW_H

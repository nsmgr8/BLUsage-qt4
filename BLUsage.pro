#-------------------------------------------------
#
# Project created by QtCreator 2011-06-29T17:11:37
#
#-------------------------------------------------

QT       += core gui network xml

TARGET = BLUsage
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    treeitem.cpp \
    treemodel.cpp \
    blusage.cpp \
    accountdialog.cpp

HEADERS  += mainwindow.h \
    treeitem.h \
    treemodel.h \
    blusage.h \
    accountdialog.h

FORMS    += mainwindow.ui \
    accountdialog.ui

LIBS += -L/usr/lib -ltidy

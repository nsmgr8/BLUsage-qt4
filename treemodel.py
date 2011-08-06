from PySide.QtCore import (QAbstractItemModel, Qt, QModelIndex)

from treeitem import TreeItem

class TreeModel(QAbstractItemModel):

    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(['Date', 'Data (KB)', 'Data (MB)'], None)
        self.setupModel(data)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if role == Qt.DisplayRole:
            return index.internalPointer().data(index.column())

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        parentItem = index.internalPointer().parent()
        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModel(self, data):
        for daily in data:
            items = [daily.day, daily.dataUsed, daily.dataUsed / 1024.0]
            child = TreeItem(items, self.rootItem)
            self.rootItem.childItems.append(child)
            for detail in daily.detail:
                detail.append('')
                child.childItems.append(TreeItem(detail, child))


# Form implementation generated from reading ui file 'import_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName("ImportDialog")
        ImportDialog.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=ImportDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 371, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cancelButton = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 4, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 3, 1, 1)
        self.fileUrl = QtWidgets.QLineEdit(parent=self.gridLayoutWidget)
        self.fileUrl.setObjectName("fileUrl")
        self.gridLayout_2.addWidget(self.fileUrl, 0, 3, 1, 1)
        self.OkButton = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.OkButton.setObjectName("OkButton")
        self.gridLayout_2.addWidget(self.OkButton, 3, 5, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.chooseFile = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.chooseFile.setObjectName("chooseFile")
        self.gridLayout_2.addWidget(self.chooseFile, 0, 5, 1, 1)
        self.delimerList = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.delimerList.setObjectName("delimerList")
        self.delimerList.addItem("")
        self.delimerList.addItem("")
        self.delimerList.addItem("")
        self.delimerList.addItem("")
        self.gridLayout_2.addWidget(self.delimerList, 1, 3, 1, 1)
        self.lineBreakList = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.lineBreakList.setObjectName("lineBreakList")
        self.lineBreakList.addItem("")
        self.lineBreakList.addItem("")
        self.lineBreakList.addItem("")
        self.gridLayout_2.addWidget(self.lineBreakList, 2, 3, 1, 1)

        self.retranslateUi(ImportDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)

    def retranslateUi(self, ImportDialog):
        _translate = QtCore.QCoreApplication.translate
        ImportDialog.setWindowTitle(_translate("ImportDialog", "Dialog"))
        self.cancelButton.setText(_translate("ImportDialog", "取消"))
        self.label_3.setText(_translate("ImportDialog", "换行符"))
        self.label_2.setText(_translate("ImportDialog", "分隔符"))
        self.OkButton.setText(_translate("ImportDialog", "确定"))
        self.label.setText(_translate("ImportDialog", "文件路径"))
        self.chooseFile.setText(_translate("ImportDialog", "浏览"))
        self.delimerList.setItemText(0, _translate("ImportDialog", "空格"))
        self.delimerList.setItemText(1, _translate("ImportDialog", "逗号 (,)"))
        self.delimerList.setItemText(2, _translate("ImportDialog", "分号 (;)"))
        self.delimerList.setItemText(3, _translate("ImportDialog", "制表符 (\\\\t)"))
        self.lineBreakList.setItemText(0, _translate("ImportDialog", "\\\\n"))
        self.lineBreakList.setItemText(1, _translate("ImportDialog", "\\\\r\\\\n"))
        self.lineBreakList.setItemText(2, _translate("ImportDialog", "\\\\r"))
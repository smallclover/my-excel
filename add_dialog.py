# Form implementation generated from reading ui file 'add_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(412, 307)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 371, 281))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 331, 228))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.work_start_time = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.work_start_time.setObjectName("work_start_time")
        self.work_start_time.addItem("")
        self.work_start_time.addItem("")
        self.work_start_time.addItem("")
        self.verticalLayout.addWidget(self.work_start_time)
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.work_end_time = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.work_end_time.setObjectName("work_end_time")
        self.work_end_time.addItem("")
        self.work_end_time.addItem("")
        self.work_end_time.addItem("")
        self.work_end_time.addItem("")
        self.verticalLayout.addWidget(self.work_end_time)
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.work_content = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.work_content.setObjectName("work_content")
        self.verticalLayout.addWidget(self.work_content)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(19, 230, 331, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "勤务"))
        self.titleLabel.setText(_translate("Dialog", "追加"))
        self.label.setText(_translate("Dialog", "开始时间"))
        self.work_start_time.setItemText(0, _translate("Dialog", "9:00"))
        self.work_start_time.setItemText(1, _translate("Dialog", "10:00"))
        self.work_start_time.setItemText(2, _translate("Dialog", "11:00"))
        self.label_2.setText(_translate("Dialog", "结束时间"))
        self.work_end_time.setItemText(0, _translate("Dialog", "18:00"))
        self.work_end_time.setItemText(1, _translate("Dialog", "19:00"))
        self.work_end_time.setItemText(2, _translate("Dialog", "20:00"))
        self.work_end_time.setItemText(3, _translate("Dialog", "21:00"))
        self.label_3.setText(_translate("Dialog", "工作内容"))
        self.okButton.setText(_translate("Dialog", "确认"))
        self.cancelButton.setText(_translate("Dialog", "取消"))
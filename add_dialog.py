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
        Dialog.resize(423, 368)
        self.groupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 381, 341))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 331, 304))
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
        self.label_4 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AddYear = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.AddYear.setObjectName("AddYear")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.AddYear.addItem("")
        self.horizontalLayout_3.addWidget(self.AddYear)
        self.label_7 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.AddMonth = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.AddMonth.setObjectName("AddMonth")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.AddMonth.addItem("")
        self.horizontalLayout_3.addWidget(self.AddMonth)
        self.label_5 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.AddDay = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.AddDay.setObjectName("AddDay")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.AddDay.addItem("")
        self.horizontalLayout_3.addWidget(self.AddDay)
        self.label_6 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "勤务"))
        self.titleLabel.setText(_translate("Dialog", "追加"))
        self.label_4.setText(_translate("Dialog", "日期"))
        self.AddYear.setItemText(0, _translate("Dialog", "2024"))
        self.AddYear.setItemText(1, _translate("Dialog", "2025"))
        self.AddYear.setItemText(2, _translate("Dialog", "2026"))
        self.AddYear.setItemText(3, _translate("Dialog", "2027"))
        self.AddYear.setItemText(4, _translate("Dialog", "2028"))
        self.AddYear.setItemText(5, _translate("Dialog", "2029"))
        self.AddYear.setItemText(6, _translate("Dialog", "2030"))
        self.label_7.setText(_translate("Dialog", "年"))
        self.AddMonth.setItemText(0, _translate("Dialog", "01"))
        self.AddMonth.setItemText(1, _translate("Dialog", "02"))
        self.AddMonth.setItemText(2, _translate("Dialog", "03"))
        self.AddMonth.setItemText(3, _translate("Dialog", "04"))
        self.AddMonth.setItemText(4, _translate("Dialog", "05"))
        self.AddMonth.setItemText(5, _translate("Dialog", "06"))
        self.AddMonth.setItemText(6, _translate("Dialog", "07"))
        self.AddMonth.setItemText(7, _translate("Dialog", "08"))
        self.AddMonth.setItemText(8, _translate("Dialog", "09"))
        self.AddMonth.setItemText(9, _translate("Dialog", "10"))
        self.AddMonth.setItemText(10, _translate("Dialog", "11"))
        self.AddMonth.setItemText(11, _translate("Dialog", "12"))
        self.label_5.setText(_translate("Dialog", "月"))
        self.AddDay.setItemText(0, _translate("Dialog", "01"))
        self.AddDay.setItemText(1, _translate("Dialog", "02"))
        self.AddDay.setItemText(2, _translate("Dialog", "03"))
        self.AddDay.setItemText(3, _translate("Dialog", "04"))
        self.AddDay.setItemText(4, _translate("Dialog", "05"))
        self.AddDay.setItemText(5, _translate("Dialog", "06"))
        self.AddDay.setItemText(6, _translate("Dialog", "07"))
        self.AddDay.setItemText(7, _translate("Dialog", "08"))
        self.AddDay.setItemText(8, _translate("Dialog", "09"))
        self.AddDay.setItemText(9, _translate("Dialog", "10"))
        self.AddDay.setItemText(10, _translate("Dialog", "11"))
        self.AddDay.setItemText(11, _translate("Dialog", "12"))
        self.AddDay.setItemText(12, _translate("Dialog", "13"))
        self.AddDay.setItemText(13, _translate("Dialog", "14"))
        self.AddDay.setItemText(14, _translate("Dialog", "15"))
        self.AddDay.setItemText(15, _translate("Dialog", "16"))
        self.AddDay.setItemText(16, _translate("Dialog", "17"))
        self.AddDay.setItemText(17, _translate("Dialog", "18"))
        self.AddDay.setItemText(18, _translate("Dialog", "19"))
        self.AddDay.setItemText(19, _translate("Dialog", "20"))
        self.AddDay.setItemText(20, _translate("Dialog", "21"))
        self.AddDay.setItemText(21, _translate("Dialog", "22"))
        self.AddDay.setItemText(22, _translate("Dialog", "23"))
        self.AddDay.setItemText(23, _translate("Dialog", "24"))
        self.AddDay.setItemText(24, _translate("Dialog", "25"))
        self.AddDay.setItemText(25, _translate("Dialog", "26"))
        self.AddDay.setItemText(26, _translate("Dialog", "27"))
        self.AddDay.setItemText(27, _translate("Dialog", "28"))
        self.AddDay.setItemText(28, _translate("Dialog", "29"))
        self.AddDay.setItemText(29, _translate("Dialog", "30"))
        self.AddDay.setItemText(30, _translate("Dialog", "31"))
        self.label_6.setText(_translate("Dialog", "日"))
        self.label.setText(_translate("Dialog", "开始时间"))
        self.work_start_time.setItemText(0, _translate("Dialog", "09:00:00"))
        self.work_start_time.setItemText(1, _translate("Dialog", "10:00:00"))
        self.work_start_time.setItemText(2, _translate("Dialog", "11:00:00"))
        self.label_2.setText(_translate("Dialog", "结束时间"))
        self.work_end_time.setItemText(0, _translate("Dialog", "18:00:00"))
        self.work_end_time.setItemText(1, _translate("Dialog", "19:00:00"))
        self.work_end_time.setItemText(2, _translate("Dialog", "20:00:00"))
        self.work_end_time.setItemText(3, _translate("Dialog", "21:00:00"))
        self.label_3.setText(_translate("Dialog", "工作内容"))
        self.okButton.setText(_translate("Dialog", "确认"))
        self.cancelButton.setText(_translate("Dialog", "取消"))

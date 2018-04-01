/********************************************************************************
** Form generated from reading UI file 'earthQuakeGUI.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_EARTHQUAKEGUI_H
#define UI_EARTHQUAKEGUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_earthQuakeGUIClass
{
public:

    void setupUi(QWidget *earthQuakeGUIClass)
    {
        if (earthQuakeGUIClass->objectName().isEmpty())
            earthQuakeGUIClass->setObjectName(QStringLiteral("earthQuakeGUIClass"));
        earthQuakeGUIClass->resize(600, 400);

        retranslateUi(earthQuakeGUIClass);

        QMetaObject::connectSlotsByName(earthQuakeGUIClass);
    } // setupUi

    void retranslateUi(QWidget *earthQuakeGUIClass)
    {
        earthQuakeGUIClass->setWindowTitle(QApplication::translate("earthQuakeGUIClass", "earthQuakeGUI", nullptr));
    } // retranslateUi

};

namespace Ui {
    class earthQuakeGUIClass: public Ui_earthQuakeGUIClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_EARTHQUAKEGUI_H

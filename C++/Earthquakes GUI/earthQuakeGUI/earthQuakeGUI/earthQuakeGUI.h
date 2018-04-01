#pragma once

#include <QtWidgets/QWidget>
#include "ui_earthQuakeGUI.h"
#include "earthQuakes.h"
#include <QString>
#include <QPlainTextEdit>
#include <QLabel>
#include <QPushButton>
class earthQuakeGUI : public QWidget
{
	Q_OBJECT

public:
	earthQuakeGUI(QWidget *parent = Q_NULLPTR);

	protected slots:
		void getData();
		void getAverage();

private:
	Ui::earthQuakeGUIClass ui;
	EarthQuakes earthQuakes;
	QLabel* textoutput;
};

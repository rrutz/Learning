#pragma once

#include <QtWidgets/QWidget>
#include "ui_earthQuakeGUI.h"
#include "earthQuakes.h"
#include <QString>
#include <QPlainTextEdit>
#include <QLabel>
#include "descriptive_Descriptions_Pannel.h"
#include <QPushButton>
#include "worldMapPannel.h"
#include "histogram.h"

class earthQuakeGUI : public QWidget
{
	Q_OBJECT

public:
	earthQuakeGUI(QWidget *parent = Q_NULLPTR);

	protected slots:
		void getDS();

public:
	Ui::earthQuakeGUIClass ui;
	EarthQuakes earthQuakes;
	descriptive_Descriptions_Pannel* DS_Panel;
	WorldMapPannel* worldMap;
	WorldMapPannel* worldMap1;
	Histogram* hist;
};

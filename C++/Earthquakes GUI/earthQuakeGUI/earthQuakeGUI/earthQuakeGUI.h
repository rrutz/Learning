#pragma once

#include <QtWidgets/QWidget>
#include "ui_earthQuakeGUI.h"
#include "earthQuakes.h"
#include "descriptive_Descriptions_Pannel.h"
#include "worldMapPannel.h"
#include "histogram.h"
#include "slidersPannel.h"
#include <QLabel>

class earthQuakeGUI : public QWidget
{
	Q_OBJECT

public:
	earthQuakeGUI(QWidget *parent = Q_NULLPTR);

	protected slots:
		void minChanged( int newMin);
		void maxChanged(int newMax);
		void minChanged_year(int newMin);
		void maxChanged_year(int newMax);

private:
	Ui::earthQuakeGUIClass ui;
	EarthQuakes earthQuakes;
	descriptive_Descriptions_Pannel* DS_Panel;
	WorldMapPannel* worldMap;
	Histogram* hist;
	SliderPannel* sliderPannel;
	SliderPannel* sliderPannel_year;
	QLabel* title = new QLabel("Earthquakes");
};

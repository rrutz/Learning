#include "earthQuakeGUI.h"
#include <QGridLayout>

earthQuakeGUI::earthQuakeGUI(QWidget *parent)
	:
	QWidget(parent),
	earthQuakes(EarthQuakes("database.csv")),
	worldMap( new WorldMapPannel(&earthQuakes)),
	DS_Panel(new descriptive_Descriptions_Pannel(&earthQuakes)),
	hist( new Histogram(&earthQuakes))
	
{
	ui.setupUi(this);
	this->showMaximized();
	this->setStyleSheet("background-color: black");

	// foramt title
	title->setStyleSheet("color: white; font: 35pt");

	// add magitude slider
	sliderPannel = new SliderPannel(0, 10, "Magnitude");
	connect(sliderPannel, SIGNAL(sliderMinChanged(int)), this, SLOT(minChanged(int)));
	connect(sliderPannel, SIGNAL(sliderMaxChanged(int)), this, SLOT(maxChanged(int)));

	// add year slider
	sliderPannel_year = new SliderPannel(1960, 2020, "Year");
	connect(sliderPannel_year, SIGNAL(sliderMinChanged(int)), this, SLOT(minChanged_year(int)));
	connect(sliderPannel_year, SIGNAL(sliderMaxChanged(int)), this, SLOT(maxChanged_year(int)));


	// add widgets to window
	QGridLayout* mainLayout = new QGridLayout(this);
	mainLayout->addWidget(title, 0, 0,1,2, Qt::AlignCenter);
	mainLayout->addWidget(worldMap, 1, 0);
	mainLayout->addWidget(hist, 1, 1);
	mainLayout->addWidget(sliderPannel, 2, 0, 1, 2);
	mainLayout->addWidget(sliderPannel_year, 3, 0, 1, 2);
	mainLayout->addWidget(DS_Panel, 4, 0, 1, 1);
}

void earthQuakeGUI::minChanged(int newMin)
{
	earthQuakes.rangeMagMin = newMin;
	DS_Panel->getDS();
	hist->draw();
	worldMap->draw();
}

void earthQuakeGUI::maxChanged(int newMax)
{
	earthQuakes.rangeMagMax = newMax;
	DS_Panel->getDS();
	hist->draw();
	worldMap->draw();
}


void earthQuakeGUI::minChanged_year(int newMin)
{
	earthQuakes.rangeMagMin_year = newMin;
	DS_Panel->getDS();
	hist->draw();
	worldMap->draw();
}

void earthQuakeGUI::maxChanged_year(int newMax)
{
	earthQuakes.rangeMagMax_year = newMax;
	DS_Panel->getDS();
	hist->draw();
	worldMap->draw();
}


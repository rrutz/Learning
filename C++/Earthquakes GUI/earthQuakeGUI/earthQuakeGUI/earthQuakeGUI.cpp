#include "earthQuakeGUI.h"
#include <QPushButton>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QSignalMapper>
#include <QAction>
#include <QDebug>
#include <QSlider>



earthQuakeGUI::earthQuakeGUI(QWidget *parent)
	:
	QWidget(parent),
	earthQuakes(EarthQuakes("database.csv")),
	worldMap( new WorldMapPannel(&earthQuakes)),
	DS_Panel(new descriptive_Descriptions_Pannel(&earthQuakes)),
	hist( new Histogram(&earthQuakes)),
	sliderPannel( new SliderPannel(0,10))
{
	ui.setupUi(this);
	this->showMaximized();
	this->setStyleSheet("background-color: black");

	//QPushButton* getAvgB = new QPushButton("Get avg");
	//getAvgB->setGeometry(0, 0, 100, 50);
	//getAvgB->setStyleSheet("background-color: white");
	//connect(getAvgB, SIGNAL(clicked()), this, SLOT(getDS()));

	QGridLayout* mainLayout = new QGridLayout(this);
	mainLayout->addWidget(worldMap, 0, 0);
	mainLayout->addWidget(hist, 0, 1);
	//mainLayout->addWidget(getAvgB, 2, 0);
	mainLayout->addWidget(DS_Panel, 2, 1);


	connect(sliderPannel, SIGNAL(sliderMinChanged(int)), this, SLOT(minChanged(int)));
	connect(sliderPannel, SIGNAL(sliderMaxChanged(int)), this, SLOT(maxChanged(int)));
	mainLayout->addWidget(sliderPannel, 1, 0,1,2);
	

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

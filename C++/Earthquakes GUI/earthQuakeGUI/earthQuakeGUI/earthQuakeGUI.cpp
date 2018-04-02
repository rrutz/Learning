#include "earthQuakeGUI.h"
#include <QPushButton>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QSignalMapper>
#include <QAction>
#include <QDebug>


earthQuakeGUI::earthQuakeGUI(QWidget *parent)
	:
	QWidget(parent),
	earthQuakes(EarthQuakes("database.csv"))
{
	DS_Panel = new descriptive_Descriptions_Pannel(&earthQuakes);

	ui.setupUi(this);
	this->showMaximized();
	this->setStyleSheet("background-color: black");

	QGridLayout* mainLayout = new QGridLayout(this);
	mainLayout->addWidget(worldMap, 0, 0);

	WorldMapPannel* worldMap1 = new WorldMapPannel();
	mainLayout->addWidget(worldMap1, 0, 1);


	QPushButton* getAvgB = new QPushButton("Get avg");
	getAvgB->setGeometry(0, 0, 100, 50);
	getAvgB->setStyleSheet("background-color: white");
	connect(getAvgB, SIGNAL(clicked()), this, SLOT(getDS()));
	mainLayout->addWidget(getAvgB, 1, 0);
	mainLayout->addWidget(DS_Panel,1,1);
}


void earthQuakeGUI::getData()
{
	
}

void earthQuakeGUI::getDS()
{
	DS_Panel->getDS();
}

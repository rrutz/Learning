#include "earthQuakeGUI.h"
#include <QPushButton>
#include <QVBoxLayout>
#include <QSignalMapper>
#include <QAction>
#include <QDebug>

earthQuakeGUI::earthQuakeGUI(QWidget *parent)
	: 
	QWidget(parent)
{
	ui.setupUi(this);
	this->showMaximized();
	this->setStyleSheet("background-color: black");

	QVBoxLayout* mainLayout = new QVBoxLayout(this);

	QPushButton* loadFileB = new QPushButton( "Load Data" );
	loadFileB->setGeometry(0, 0, 100, 50);
	loadFileB->setStyleSheet("background-color: white");
	connect(loadFileB, SIGNAL(clicked()), this, SLOT(getData()));
	mainLayout->addWidget(loadFileB);

	textoutput = new QLabel();
	textoutput->setText("fuck yeah ");
	textoutput->setStyleSheet("background-color: black; color: white");
	mainLayout->addWidget(textoutput);

	QPushButton* getAvgB = new QPushButton("Get avg");
	getAvgB->setGeometry(0, 0, 100, 50);
	getAvgB->setStyleSheet("background-color: white");
	connect(getAvgB, SIGNAL(clicked()), this, SLOT(getAverage()));
	mainLayout->addWidget(getAvgB);
}

void earthQuakeGUI::getData()
{
	earthQuakes = EarthQuakes("database.csv");
}

void earthQuakeGUI::getAverage()
{
	QString avg = QString::number( earthQuakes.average() );
	textoutput->setText(avg);
}


#include "descriptive_Descriptions_Pannel.h"

descriptive_Descriptions_Pannel::descriptive_Descriptions_Pannel(EarthQuakes* earthQuakes, QWidget *parent)
	:
	QWidget(parent),
	earthQuakes( earthQuakes )
{
	layout = new QGridLayout(this);
	addLabel(0, 0, textM, "Mean magnitude");
	addLabel(0, 1, textM_value, "");
	addLabel(1, 0, textV, "Variance magnitude");
	addLabel(1, 1, textV_value, "");
	addLabel(2, 0, textC, "Count");
	addLabel(2, 1, textC_value, "");
}

void descriptive_Descriptions_Pannel::getDS()
{
	textM_value->setText(QString::number(earthQuakes->average()));
	textV_value->setText(QString::number(earthQuakes->variance()));
	textC_value->setText(QString::number(earthQuakes->count()));
}

void descriptive_Descriptions_Pannel::addLabel(int row, int col, QLabel* label, QString message)
{
	label->setText(message);
	label->setStyleSheet("background-color: black; color: white");
	layout->addWidget(label, row, col);
}



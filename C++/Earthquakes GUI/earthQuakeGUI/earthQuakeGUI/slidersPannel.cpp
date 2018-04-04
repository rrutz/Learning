#include "slidersPannel.h"
#include <QLabel>
#include <QDebug>

SliderPannel::SliderPannel(int min, int max, QString name, QWidget* parent )
	:
	QWidget(parent),
	sliderMin( new QSlider(Qt::Horizontal, 0)),
	sliderMax( new QSlider(Qt::Horizontal, 0)),
	min(min), max(max)
{
	layout = new QGridLayout(this);

	formatSlider(sliderMin, min, 0, "Min "+name);
	addLabels(sliderMin, 0);

	formatSlider(sliderMax, max, 6, "Max " + name);
	addLabels(sliderMin, 6);

	connect(sliderMin, SIGNAL(valueChanged(int)), this, SLOT(sendMinSignal( int )));
	connect(sliderMax, SIGNAL(valueChanged(int)), this, SLOT(sendMaxSignal(int)));
}

void SliderPannel::formatSlider(QSlider* slider, int sliderPosition, int col, QString name)
{
	QLabel* Qlabel_name = new QLabel(name);
	Qlabel_name->setStyleSheet("font:20pt; color:white");
	layout->addWidget(Qlabel_name, 0, col, 1, 6, Qt::AlignCenter );


	slider->setMaximum(max);
	slider->setMinimum(min);
	slider->setTickInterval((max - min) / 5);
	slider->setSliderPosition(sliderPosition);
	slider->setTickPosition(QSlider::TicksBothSides);
	layout->addWidget(slider, 1, col, 1, 6);
}

void SliderPannel::addLabels(QSlider * slider, int col)
{
	int interval = (max - min) / 5;
	for (int i = 0; i < 6; i++)
	{
		QLabel* mark = new QLabel(QString::number(min+i * interval));
		mark->setStyleSheet("background-color: black; color: white");

		if (i == 5)
		{
			mark->setFixedWidth(20);
		}
		layout->addWidget(mark, 2, i+col);
	}
}


void SliderPannel::sendMinSignal(int newMin)
{
	emit sliderMinChanged(newMin);
}

void SliderPannel::sendMaxSignal(int newMax)
{
	emit sliderMaxChanged(newMax);
}




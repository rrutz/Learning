#include "slidersPannel.h"
#include <QLabel>
#include <QDebug>

SliderPannel::SliderPannel(int min, int max, QWidget* parent )
	:
	QWidget(parent),
	sliderMin( new QSlider(Qt::Horizontal, 0)),
	sliderMax( new QSlider(Qt::Horizontal, 0))
{
	layout = new QGridLayout(this);
	formatSlider(sliderMin, min, 0);
	addLabels(sliderMin, 0);

	formatSlider(sliderMax, max, 6);
	addLabels(sliderMin, 6);

	connect(sliderMin, SIGNAL(valueChanged(int)), this, SLOT(sendMinSignal( int )));
	connect(sliderMax, SIGNAL(valueChanged(int)), this, SLOT(sendMaxSignal(int)));
}

void SliderPannel::formatSlider(QSlider* slider, int sliderPosition, int col)
{
	slider->setMaximum(10);
	slider->setMinimum(0);
	slider->setTickInterval(0.5);
	slider->setSliderPosition(sliderPosition);
	slider->setTickPosition(QSlider::TicksBothSides);
	layout->addWidget(slider, 0, col, 1, 6);
}

void SliderPannel::addLabels(QSlider * slider, int col)
{
	for (int i = 0; i < 6; i++)
	{
		QLabel* mark = new QLabel(QString::number(i * 2));
		mark->setStyleSheet("background-color: black; color: white");

		if (i == 5)
		{
			mark->setFixedWidth(15);
		}
		layout->addWidget(mark, 1, i+col);
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




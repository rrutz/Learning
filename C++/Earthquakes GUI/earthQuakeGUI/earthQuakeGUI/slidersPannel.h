#pragma once
#include <QtWidgets/QWidget>
#include <QSlider>
#include <QGridLayout>

class SliderPannel : public QWidget
{
	Q_OBJECT
public:
	SliderPannel(int min, int max, QWidget* parent = Q_NULLPTR);

private:
	void formatSlider(QSlider* slider, int sliderPosition, int col);
	void addLabels(QSlider* slider, int col);

private:

	QSlider* sliderMin;
	QSlider* sliderMax;
	QGridLayout* layout;

protected slots:
	void sendMinSignal(int newValue);
	void sendMaxSignal(int newValue);

signals:
	void sliderMinChanged( int newMin );
	void sliderMaxChanged( int newMax );
};



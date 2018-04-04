#pragma once

#include <QtWidgets/QWidget>
#include <QLabel>
#include "earthQuakes.h"
#include <string>
#include <QGridLayout>

class descriptive_Descriptions_Pannel : public QWidget
{
	Q_OBJECT

public:
	descriptive_Descriptions_Pannel(EarthQuakes* earthQuakes, QWidget *parent = Q_NULLPTR );
	void getDS();

private:
	void addLabel(int row, int col, QLabel* label, QString message);
	

private:
	EarthQuakes* earthQuakes;
	QLabel* textM = new QLabel();
	QLabel* textM_value = new QLabel();
	QLabel* textV = new QLabel();
	QLabel* textV_value = new QLabel();
	QLabel* textC = new QLabel();
	QLabel* textC_value = new QLabel();
	QGridLayout* layout;

};

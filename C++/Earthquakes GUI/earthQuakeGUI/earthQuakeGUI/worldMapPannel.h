#pragma once
#include "worrldMapData.h"
#include <QImage>
#include <QLabel>
#include "earthQuakes.h"

class WorldMapPannel : public QLabel
{
public:
	WorldMapPannel(EarthQuakes* earthQuakes);
private:
	void draw();

public:
	WorldMap* worldMapData = new WorldMap();

private:
	QImage map;
	EarthQuakes* earthQuakes;
};

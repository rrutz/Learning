#pragma once
#include "worrldMapData.h"
#include <QImage>
#include <QLabel>

class WorldMapPannel : public QLabel
{
public:
	WorldMapPannel();
private:
	void draw();

public:
	WorldMap* worldMapData = new WorldMap();

private:
	QImage map;

};

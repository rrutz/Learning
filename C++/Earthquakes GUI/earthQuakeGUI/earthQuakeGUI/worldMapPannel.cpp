#include "worldMapPannel.h"
#include <cmath>
#include <QDebug>
WorldMapPannel::WorldMapPannel()
{
	map =  QImage(800,400, QImage::Format_RGB32);
	draw();
	this->setPixmap(QPixmap::fromImage(map));
}

void WorldMapPannel::draw()
{
	float x_scale = map.width()  / (worldMapData->maxLong - worldMapData->minLong);
	float y_scale = map.height() / (worldMapData->maxLat - worldMapData->minLat);
	float scale = std::min(x_scale, y_scale);

	for( auto col = worldMapData->worldMap.begin(); col < worldMapData->worldMap.end(); col ++)
	{
		int y = static_cast<int>(   (col->latidute - worldMapData->minLat) * scale);
		int x = static_cast<int>(   (col->longitude - worldMapData->minLong) * scale);
		map.setPixel(x, y, (90, 90, 90));
	}
}

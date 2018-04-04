#include "worldMapPannel.h"
#include <cmath>
#include <QDebug>
WorldMapPannel::WorldMapPannel(EarthQuakes* earthQuakes)
	:
	earthQuakes(earthQuakes)
{
	
	draw();
	
}

void WorldMapPannel::draw()
{
	
	map = QImage(800, 400, QImage::Format_RGB32);

	float x_scale = map.width()  / (worldMapData->maxLong - worldMapData->minLong+50);
	float y_scale = map.height() / (worldMapData->maxLat - worldMapData->minLat+50);
	float scale = std::min(x_scale, y_scale);

	for( auto col = worldMapData->worldMap.begin(); col < worldMapData->worldMap.end(); col ++)
	{
		int y = static_cast<int>(   (col->latidute - worldMapData->minLat) * scale)+25;
		int x = static_cast<int>(   (col->longitude - worldMapData->minLong) * scale)+25;
		map.setPixel(x, y, (0, 0, 0));
	}

	if (earthQuakes->rangeMagMin >= earthQuakes->rangeMagMax)
	{
		this->setPixmap(QPixmap::fromImage(map));
		return;
	}

	for (auto col = earthQuakes->earthquakes.begin(); col < earthQuakes->earthquakes.end(); col++)
	{
		if (col->magnitude < earthQuakes->rangeMagMin || col->magnitude > earthQuakes->rangeMagMax)
			continue;
		if (col->year < earthQuakes->rangeMagMin_year || col->year > earthQuakes->rangeMagMax_year)
			continue;
		int y = static_cast<int>((col->latitude - worldMapData->minLat) * scale)+25;
		int x = static_cast<int>((col->longitude - worldMapData->minLong) * scale)+25;
		map.setPixel(x, y, qRgb(255,0,0));
	}

	this->setPixmap(QPixmap::fromImage(map));
}

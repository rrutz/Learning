#pragma once
#include <QLabel>
#include <QImage>
#include "earthQuakes.h"
#include <vector>
#include <algorithm>

class Histogram : public QLabel
{
public:
	Histogram(EarthQuakes* earthQuakes)
		:
		earthQuakes(earthQuakes)
	{
		map = QImage(800, 400, QImage::Format_RGB32);
		draw();	
	}

public:
	void draw()
	{
		map = QImage(800, 400, QImage::Format_RGB32);
		float binNum = 10;
		float min = earthQuakes->rangeMagMin;
		float max = earthQuakes->rangeMagMax;
		float minYear = earthQuakes->rangeMagMin_year;
		float maxYear = earthQuakes->rangeMagMax_year;
	
		float binWidth = (max - min) / binNum;
		std::vector<int> binSize;
		for (int bin = 0; bin < binNum; bin++)
		{
			int mycount = std::count_if(earthQuakes->earthquakes.begin(), earthQuakes->earthquakes.end(), 
						[min, binWidth, bin, minYear, maxYear](EarthQuakes::EarthQuake x)
							{ return(	x.magnitude >= min + binWidth * bin && 
										x.magnitude < min + binWidth * (bin + 1)) &&
										x.year >= minYear && 
										x.year <= maxYear;  });
			binSize.push_back(mycount);
		}

		
		// draw x-axis and ticks
		for (int bin = 0; bin < binNum; bin++)
		{
			float binWidth = 50;// static_cast<float>((this->width() - 50)) / binNum;
			int xLeft = 50 + bin * binWidth;
			int xRight = 50 + (bin + 1) * binWidth;
			for (int x = xLeft; x <= xRight; x++)
			{
				map.setPixel(x, map.height() - 50, 0);
			}

			//tick marks
			for (int y = map.height() - 45; y >= map.height() - 55; y--)
			{
				map.setPixel(xRight - 1, y, qRgb(255, 0, 0));
				map.setPixel(xRight, y, qRgb(255, 0, 0));
				map.setPixel(xRight + 1, y, qRgb(255, 0, 0));
				map.setPixel(xLeft - 1, y, qRgb(255, 0, 0));
				map.setPixel(xLeft, y, qRgb(255, 0, 0));
				map.setPixel(xLeft + 1, y, qRgb(255, 0, 0));
			}
		}

		float maxCount = *std::max_element(binSize.begin(), binSize.end());
		if (min >= max || maxCount <= 0)
		{
			this->setPixmap(QPixmap::fromImage(map));
			return;
		}

		// draw boxes
		float y_scale = (static_cast<float>(map.height()) - 100) / maxCount;
		for (int bin = 0; bin < binNum; bin++)
		{
			float binWidth = 50;// static_cast<float>((this->width() - 50)) / binNum;
			int yTop = map.height() - static_cast<int>(binSize[bin] * y_scale)-50;
			int xLeft = 50+bin * binWidth;
			int xRight = 50+(bin + 1) * binWidth;
			for (int y = map.height() - 50; y >= yTop; y--)
			{
				map.setPixel(xLeft, y, 0);
			}
			for (int y = map.height() - 50; y >= yTop; y--)
			{
				map.setPixel(xRight, y, 0);
			}
			for (int x = xLeft; x <= xRight; x++)
			{
				map.setPixel(x, yTop, 0);
			}
		}
		this->setPixmap(QPixmap::fromImage(map));
	}
private:
	EarthQuakes* earthQuakes;
	QImage map;
};
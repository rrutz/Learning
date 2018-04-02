#include "earthQuakes.h"
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>  
#include <iomanip>  
#include <cmath>
EarthQuakes::EarthQuake::EarthQuake(int year, float latitude, float longitude, float dept, float magnitude)
	:
	year(year),
	latitude(latitude),
	longitude(longitude),
	dept(dept),
	magnitude(magnitude)
{}

EarthQuakes::EarthQuakes(std::string fileIn)
{
	std::ifstream file_in(fileIn);
	std::string str;

	int i = 0;
	for (int lineNum = 0; file_in.good(), i <100; lineNum++, i++)
	{
		std::getline(file_in, str);
		if (lineNum == 0 || str == "")
			continue;

		std::istringstream line(str, ',');
		std::string v;
		int year;
		float latitude, longitude, dept, magnitude;
		for (int col = 0; col < 9, line.good(); col++)
		{
			std::getline(line, v, ',');
			if (col == 0)
			{
				std::string date;
				std::istringstream date_stream(v);
				std::getline(date_stream, date, '/');
				std::getline(date_stream, date, '/');
				std::getline(date_stream, date, '/');
				if (date != "")
					year = stoi(date);
			}
			else if (col == 2)
			{
				latitude = std::stof(v);
			}
			else if (col == 3)
			{
				longitude = std::stof(v);
			}
			else if (col == 5)
			{
				dept = std::stof(v);
			}
			else if (col == 8)
			{
				magnitude = std::stof(v);
			}
		}
		earthquakes.push_back(EarthQuake(year, latitude, longitude, dept, magnitude));
	}
}

void EarthQuakes::print()
{
	int i = 0;

	for (auto quake = earthquakes.begin(); quake < earthquakes.end(), i < 50; quake++, i++)
	{
		std::cout << "Year:" << std::setw(5) << quake->year << std::setw(7) << "  Latitude: " << std::setw(7) << quake->latitude << "  Longitude: " << std::setw(8) << quake->longitude
			<< "  Magnitude: " << std::setw(7) << quake->magnitude
			<< std::endl;
	}
}

float EarthQuakes::average()
{
	float sum = 0;
	float count = 0;
	for (auto quake = earthquakes.begin(); quake < earthquakes.end(); quake++)
	{
		count++;
		sum += quake->magnitude;
	}
	return sum / count;
}

float EarthQuakes::variance()
{
	float sum_x2 = 0;
	float sum_x = 0;
	float n = 0;
	for (auto quake = earthquakes.begin(); quake < earthquakes.end(); quake++)
	{
		sum_x2 += pow(quake->magnitude, 2);
		sum_x += quake->magnitude;
		n++;
	}
	float mean = sum_x / n;
	float var = (sum_x2 - 2 * mean* sum_x + pow(mean, 2)*n)/n;
	return var;
}

#pragma once
#include <fstream>
#include <string>
#include <sstream> 
#include <vector>

class WorldMap
{
private:
	struct item
	{
		float longitude;
		float latidute;
		float group;
	};

public:
	std::vector< item > worldMap;
	float minLong = 0;
	float minLat = 0;
	float maxLong = 0;
	float maxLat = 0;

public:
	WorldMap()
	{
		std::ifstream file_in("worldMap.csv");

		for (int lineNum = 0; file_in.good(); lineNum++ )
		{
			std::string line;
			std::getline(file_in, line);
			if (lineNum == 0 || line == "")
				continue;

			std::istringstream line_stream(line, ',');
			std::string cellContext;
			float longitude, latidute, group;

			std::getline(line_stream, cellContext, ',');
			longitude = std::stof(cellContext);

			std::getline(line_stream, cellContext, ',');
			latidute = std::stof(cellContext);

			std::getline(line_stream, cellContext, ',');
			group = std::stof(cellContext);
			worldMap.push_back({ longitude, -latidute, group });
		}

		getExtremes();
	}

	void getExtremes()
	{
		for (auto row = worldMap.begin(); row < worldMap.end(); row++)
		{
			if (row->latidute < minLat)
				minLat = row->latidute;
			if (row->latidute > maxLat)
				maxLat = row->latidute;

			if (row->longitude < minLong)
				minLong = row->longitude;
			if (row->longitude > maxLong)
				maxLong = row->longitude;
		}
	}
	void getMin();
};


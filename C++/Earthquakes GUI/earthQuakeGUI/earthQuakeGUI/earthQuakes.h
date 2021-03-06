#pragma once

#include <string>
#include <vector>
class EarthQuakes
{
public:
	EarthQuakes() = default;
	EarthQuakes(std::string fileIn);
	void print();
	float average();
	float variance();
	float min();
	float max();
	int count();

	float rangeMagMin = 0;
	float rangeMagMax = 10;
	float rangeMagMin_year = 1960;
	float rangeMagMax_year = 2020;

public:
	class EarthQuake
	{
	public:
		EarthQuake(int year, float latitude, float longitude, float dept, float magnitude);

	public:
		int year;
		float latitude;
		float longitude;
		float dept;
		float magnitude;
	};

public:
	std::vector< EarthQuake > earthquakes;
};

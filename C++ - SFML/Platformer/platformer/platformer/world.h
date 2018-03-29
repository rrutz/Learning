#pragma once
#include <SFML/Graphics.hpp>
#include <vector>

class Title : public sf::RectangleShape
{
public:
	Title(bool topSolid, bool allSolid, sf::Color color, float title_width, float title_height, float xPos, float yPos);
public:
	float title_width;
	float title_height;
	float xPos;
	float yPos;
	bool topSolid;
	bool allSolid;
};

class World
{
public:
	World(int nHeight, int nWidth, float pixel_Height, float pixel_Width);
	void draw(sf::RenderWindow& window);

public:
	std::vector<Title> world;

private:
	int nHeight;
	int nWidth;
	int pixel_Height;
	int pixel_Width;
};

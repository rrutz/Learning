#pragma once

#include <SFML/Graphics.hpp>
#include <vector>

class Title : public sf::RectangleShape
{
public:
	Title(bool isSolid, sf::Color color, int title_width, int title_height, int xPos, int yPos);
public:
	float title_width;
	float title_height;
	bool isSolid;
};

class World
{
public:
	World(int nHeight, int nWidth, int pixel_Height, int pixel_Width);
	void draw(sf::RenderWindow& window);

public:
	std::vector<Title> world;

private:
	int nHeight;
	int nWidth;
	int pixel_Height;
	int pixel_Width;
};

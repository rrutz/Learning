#include "world.h"


Title::Title(bool isSolid, sf::Color color, int title_width, int title_height, int xPos, int yPos)
	:
	isSolid(isSolid),
	title_width(title_width),
	title_height(title_height),
	sf::RectangleShape(sf::RectangleShape(sf::Vector2f(title_width, title_height)))
{
	setFillColor(color);
	setPosition(xPos, yPos);
}

World::World(int nHeight, int nWidth, int pixel_Height, int pixel_Width)
	:
	nHeight(nHeight),
	nWidth(nWidth),
	pixel_Height(pixel_Height),
	pixel_Width(pixel_Width)
{
	// create ground
	int groundWidth = pixel_Width;
	int groundHeight = 80.0f;
	world.push_back(Title(true, sf::Color::Green, groundWidth, groundHeight, 0, pixel_Height - groundHeight));

	// create bricks
}

void World::draw(sf::RenderWindow& window)
{
	for (auto title = world.begin(); title != world.end(); title++)
	{
		window.draw(*title);
	}
}

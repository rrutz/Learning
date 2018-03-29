#include "world.h"

Title::Title(bool topSolid, bool allSolid, sf::Color color, float title_width, float title_height, float xPos, float yPos)
	:
	topSolid(topSolid), 
	allSolid(allSolid),
	title_width(title_width),
	title_height(title_height),
	xPos( xPos ),
	yPos( yPos ),
	sf::RectangleShape(sf::RectangleShape(sf::Vector2f(title_width, title_height)))
{
	setFillColor(color);
	setPosition(xPos, yPos);
}

World::World(int nHeight, int nWidth, float pixel_Height, float pixel_Width)
	:
	nHeight(nHeight),
	nWidth(nWidth),
	pixel_Height(pixel_Height),
	pixel_Width(pixel_Width)
{
	// create ground
	float groundWidth = pixel_Width;
	float groundHeight = 80.0f;
	world.push_back(Title(true, true, sf::Color::Green, groundWidth, groundHeight, 0, pixel_Height - groundHeight));

	// create bricks
	world.push_back(Title(true, true, sf::Color::Red, 75.0f, 200.0f, 100.0f, pixel_Height - groundHeight - 80.f));
	
	world.push_back(Title(true, false, sf::Color::Black, 100.0f, 50.0f, 300.0f, pixel_Height - groundHeight - 200.f));
	world.push_back(Title(true, false, sf::Color::Black, 100.0f, 50.0f, 100.0f, pixel_Height - groundHeight - 200.f));
	world.push_back(Title(true, false, sf::Color::Black, 100.0f, 50.0f, 500.0f, pixel_Height - groundHeight - 300.f));
	world.push_back(Title(true, true, sf::Color::Black, 100.0f, 50.0f, 700.0f, pixel_Height - groundHeight - 400.f));
	world.push_back(Title(true, true, sf::Color::Red, 100.0f, 50.0f, 550.0f, pixel_Height - groundHeight - 500.f));

	world.push_back(Title(true, true, sf::Color::Red, 25.0f, pixel_Height, 0.0f, 0.0f));
	world.push_back(Title(true, true, sf::Color::Red, 25.0f, pixel_Height, pixel_Width -25.0f, 0.0f));


	world.push_back(Title(true, true, sf::Color::Red, 10.0f, 100.0f, 900.0f, pixel_Height - groundHeight - 400.f));
	world.push_back(Title(true, false, sf::Color::Black, 400.0f, 50.0f, 900.0f, pixel_Height - groundHeight - 300.f));
}

void World::draw(sf::RenderWindow& window)
{
	for (auto title = world.begin(); title != world.end(); title++)
	{
		window.draw(*title);
	}
}

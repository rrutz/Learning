#include "world.h"
#include <iostream>
WorldObject::WorldObject(float xL, float xR, float yT, float yB, bool topSolid, bool bottomSolid, bool leftSolid, bool rightSolid, sf::Color color)
	:
	rect( Rect( xL,  xR,  yT,  yB,  topSolid,  bottomSolid,  leftSolid,  rightSolid ) ),
	sf::RectangleShape(sf::RectangleShape(sf::Vector2f(xR - xL, yB - yT)))
{
	setFillColor(color);
	setPosition(rect.xL, rect.yT);
}

World::World(int nHeight, int nWidth, float pixel_Height, float pixel_Width)
	:
	nHeight(nHeight),
	nWidth(nWidth),
	pixel_Height(pixel_Height),
	pixel_Width(pixel_Width)
{
	// create ground
	float groundHeight = 80.0f;
	world.push_back(WorldObject(0, pixel_Width, pixel_Height - groundHeight, pixel_Height, true, true, true, true, sf::Color::Green));
	
	// create walls
	world.push_back(WorldObject(0, 10, 0, pixel_Height, true, true, true, true, sf::Color::Red));
	world.push_back(WorldObject(pixel_Width-10, pixel_Width, 0, pixel_Height, true, true, true, true, sf::Color::Red));


	// create walls
	world.push_back(WorldObject(100, 150, pixel_Height-200, pixel_Height-150, true, true, true, true, sf::Color::Red));
	world.push_back(WorldObject(200, 250, pixel_Height - 200, pixel_Height - 150, true, false, false, false, sf::Color::Black));

	world.push_back(WorldObject(200, 250, pixel_Height - 200, pixel_Height - 150, true, false, false, false, sf::Color::Black));

	world.push_back(WorldObject(400, 450, 500, 550, true, false, false, false, sf::Color::Black));

	world.push_back(WorldObject(500, 650, 400, 450, true, false, false, false, sf::Color::Black));


}

void World::draw(sf::RenderWindow& window)
{
	for (auto worldObject = world.begin(); worldObject != world.end(); worldObject++)
	{
		window.draw(*worldObject);
	}
}
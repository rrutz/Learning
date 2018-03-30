#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include "rect.h"

class WorldObject : public sf::RectangleShape
{
public:
	WorldObject(float xL, float xR, float yT, float yB, bool topSolid, bool bottomSolid, bool leftSolid, bool rightSolid, sf::Color color);
public:
	Rect rect;
};

class World
{
public:
	World(int nHeight, int nWidth, float pixel_Height, float pixel_Width);
	void draw(sf::RenderWindow& window);

public:
	std::vector<WorldObject> world;

private:
	int nHeight;
	int nWidth;
	int pixel_Height;
	int pixel_Width;
};

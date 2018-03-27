#pragma once
#include "mario.h"
#include "world.h"
#include "badGuy.h"


class Game
{
public:
	Game();
	int gameLoop();

private:
	void updateWorld();
	void updateFrame();

private:
	int pixel_Height = 800;
	int pixel_Width = 1200;
	sf::RenderWindow window;

	Mario mario = Mario();
	BadGuy badGuy = BadGuy();
	BadGuy badGuy2 = BadGuy();
	World world = World(25, 50, pixel_Height, pixel_Width);
	sf::Clock clock = sf::Clock::Clock();
};
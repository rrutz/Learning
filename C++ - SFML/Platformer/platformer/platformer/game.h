#pragma once
#include "mario.h"
#include "world.h"
#include "badGuy.h"
#include <vector>


class Game
{
public:
	Game();
	int gameLoop();

private:
	void updateWorld();
	void updateFrame();
	sf::Font font = sf::Font();
	sf::Text text;
	float score = 0.0f;

private:
	int pixel_Height = 800;
	int pixel_Width = 1200;
	sf::RenderWindow window;

	Mario mario = Mario("Characters_Sprites\\Mario & Luigi.png");
	std::vector<BadGuy*> badGuys = { new BadGuy("Characters_Sprites\\Mario & Luigi.png") , new BadGuy("Characters_Sprites\\Mario & Luigi.png"), new BadGuy("Characters_Sprites\\Mario & Luigi.png")};

	//BadGuy bad = BadGuy("Characters_Sprites\\Mario & Luigi.png");
	
	World world = World(25, 50, pixel_Height, pixel_Width);
	sf::Clock clock = sf::Clock::Clock();
};
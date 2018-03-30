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
	void restartGame();

private:
	void updateWorld();
	void updateFrame();
	sf::Font font = sf::Font();
	sf::Text time_text;
	sf::Text marionext_text;
	sf::Text gameResult_text;
	float time = 0.0f;
	float nextMairoCount = 5.0f;

private:
	int pixel_Height = 800;
	int pixel_Width = 1200;
	sf::RenderWindow window;
	int n = 6;
	Mario mario = Mario("Characters_Sprites\\Mario & Luigi.png");
	std::vector<BadGuy*> badGuys; 

	World world = World(25, 50, pixel_Height, pixel_Width);
	sf::Clock clock = sf::Clock::Clock();
};
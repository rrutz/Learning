#include <SFML/Graphics.hpp>
#include "game.h"

Game::Game()
	:
	window(sf::VideoMode(pixel_Width, pixel_Height), "Kick Ass Game!")
{
}

int Game::gameLoop()
{
	while (window.isOpen())
	{
		updateWorld();
		updateFrame();
	}
	return 0;
}

void Game::updateWorld()
{
	sf::Event event;
	while (window.pollEvent(event))
	{
		if (event.type == sf::Event::Closed)
			window.close();
	}

	float dx = 0.0f;
	float dy = 1.0f;
	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
	{
		dx = 1.0f;
	}
	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
	{
		dx = -1.0f;
	}

	for (auto title = world.world.begin(); title < world.world.end(); title++)
	{
		if (title->isSolid && mario.checkCollsionY(title->getPosition().y))
		{
			dy = 0.0f;
		}
	}

	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Space))
	{
		if (dy == 0.0f)
		{
			mario.jump();
		}

	}
	mario.move(0.5, dx, dy);
}

void Game::updateFrame()
{
	window.clear(sf::Color::Blue);
	world.draw(window);
	mario.draw(window);
	window.display();
}


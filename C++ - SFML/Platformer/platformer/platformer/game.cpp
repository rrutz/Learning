#include <SFML/Graphics.hpp>
#include "game.h"
#include <iostream>

Game::Game()
	:
	window(sf::VideoMode(pixel_Width, pixel_Height), "Kick Ass Game!")
{
	clock.restart();
}

int Game::gameLoop()
{
	while (window.isOpen())
	{
		updateWorld();
		updateFrame();
		clock.restart();
	}
	return 0;
}

void Game::updateWorld()
{
	float dt = clock.getElapsedTime().asSeconds();
	sf::Event event;
	while (window.pollEvent(event))
	{
		if (event.type == sf::Event::Closed)
			window.close();
	}
	
	mario.xDir = 0.0f;
	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
	{
		mario.xDir = 1.0f;
	}
	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
	{
		mario.xDir = -1.0f;
	}

	if (sf::Keyboard::isKeyPressed(sf::Keyboard::Space))
	{
		if(mario.yDir == 0.0f)
		{
			mario.jump();
		}
	}


	badGuy.yDir = 1.0f;
	badGuy2.yDir = 1.0f;
	if (!mario.isJumping)
	{
		mario.yDir = 1.0f;
	}
	for (auto title = world.world.begin(); title < world.world.end(); title++)
	{
		if (title->topSolid)
		{
			badGuy.checkFalling(title->getGlobalBounds());
			badGuy2.checkFalling(title->getGlobalBounds());
			if (!mario.isJumping)
			{
				mario.checkFalling(title->getGlobalBounds());
			}
		}
		if (title->allSolid)
		{
			mario.checkCollsionY(title->getGlobalBounds());
			mario.checkCollsionX(title->getGlobalBounds());
			badGuy.checkCollsionX(title->getGlobalBounds());
			badGuy2.checkCollsionX(title->getGlobalBounds());
		}
	}




	mario.move(dt*1000);
	badGuy.move(dt * 1000);
	badGuy2.move(dt * 1000);
}

void Game::updateFrame()
{
	window.clear(sf::Color::Blue);
	world.draw(window);
	mario.draw(window);
	badGuy.draw(window);
	badGuy2.draw(window);
	window.display();
}


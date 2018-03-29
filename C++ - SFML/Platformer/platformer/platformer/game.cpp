#include <SFML/Graphics.hpp>
#include "game.h"
#include <iostream>


Game::Game()
	:
	window(sf::VideoMode(pixel_Width, pixel_Height), "Kick Ass Game!")
{
	font.loadFromFile("C:\\Windows\\WinSxS\\amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716\\arial.ttf");
	
	text.setPosition(sf::Vector2f(500, 500));
	text.setFont(font);
	clock.restart();
	//badGuys.push_back(new BadGuy("Characters_Sprites\\Mario & Luigi.png"));
		
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
	float dt = clock.getElapsedTime().asSeconds()*1000;
	score += dt;
	sf::Event event;
	while (window.pollEvent(event))
	{
		if (event.type == sf::Event::Closed)
			window.close();
	}	

	mario.xDir = 0.0f;
	if(mario.isAlive)
	{
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
			if (mario.yDir == 0.0f)
				mario.jump();
		}


		if (!mario.isJumping)
		{
			mario.yDir = 1.0f;
		}
		else
		{
			mario.jumping(dt);
		}

		for (auto title = world.world.begin(); title < world.world.end(); title++)
		{
			if (title->topSolid)
			{
				if (!mario.isJumping)
				{
					mario.checkFalling(title->getGlobalBounds());
				}
			}
			if (title->allSolid)
			{
				mario.checkCollsionY2( title->getGlobalBounds());
				mario.checkCollsionX2(title->xPos, title->yPos, title->title_width, title->title_height, dt);
			}
		}

		mario.walk(dt);
	}
	for (auto badGuy = badGuys.begin(); badGuy < badGuys.end(); badGuy++)
	{
		(*badGuy)->yDir = 1.0f;
		for (auto title = world.world.begin(); title < world.world.end(); title++)
		{
			if (title->topSolid)
				(*badGuy)->checkFalling(title->getGlobalBounds());
			if (title->allSolid)
				(*badGuy)->checkCollsionX2(title->xPos, title->yPos, title->title_width, title->title_height, dt);
		}
		(*badGuy)->walk(dt);

		mario.isKilled((*badGuy)->xPos, (*badGuy)->yPos, (*badGuy)->width, (*badGuy)->height, dt);
	}
}

void Game::updateFrame()
{
	window.clear(sf::Color::Blue);
	world.draw(window);

	if (mario.isAlive)
	{
		mario.draw(window);
		text.setString( "Time: " + std::to_string(score));
		window.draw(text);
	}
	else
	{
		text.setString("You suck");
		window.draw(text);
	}
	
	for (auto badGuy = badGuys.begin(); badGuy < badGuys.end(); badGuy++)
	{
		(*badGuy)->draw(window);
	}
	window.display();
}


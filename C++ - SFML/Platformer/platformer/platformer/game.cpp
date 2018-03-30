#include <SFML/Graphics.hpp>
#include "game.h"
#include <iostream>


Game::Game()
	:
	window(sf::VideoMode(pixel_Width, pixel_Height), "Kick Ass Game!")
{
	font.loadFromFile("C:\\Windows\\WinSxS\\amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_10.0.16299.15_none_956f9c221e7f8716\\arial.ttf");
	time_text.setPosition(sf::Vector2f(500, 100));
	time_text.setFont(font);
	gameResult_text.setPosition(sf::Vector2f(500, 300));
	gameResult_text.setFont(font);
	marionext_text.setPosition(sf::Vector2f(400, 200));
	marionext_text.setFont(font);
	restartGame();
}

void Game::restartGame()
{
	time = 0;
	nextMairoCount = 5;
	gameResult_text.setString("");
	n = 6;
	mario.isAlive = true;
	mario.rect.xL = 100;
	mario.rect.xR = 132;
	mario.rect.yT = 400;
	mario.rect.yB = 462;

	
	for (auto badGuy = badGuys.begin(); badGuy != badGuys.end(); badGuy++)
	{
		delete (*badGuy);
	}
	badGuys.clear();

	for (int i = 0; i < n; i++)
	{
		badGuys.push_back(new BadGuy("Characters_Sprites\\Mario & Luigi.png"));
	}
	clock.restart();
}


int Game::gameLoop()
{

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}

		if (mario.isAlive && n > 0)
		{
			updateWorld();
		}
		else
		{
			if (sf::Keyboard::isKeyPressed(sf::Keyboard::R))
			{
				restartGame();
			}
		}

		updateFrame();
	}
	return 0;
}

void Game::updateWorld()
{
	float dt = clock.restart().asSeconds();
	time += dt;
	nextMairoCount -= dt;

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
			mario.yDir = 1.0f;
		else
			mario.jumping(dt);

		for (auto title = world.world.begin(); title < world.world.end(); title++)
		{
			mario.checkCollisions(title->rect, dt);
		}
		mario.move(dt);
	}
	
	
	for (auto badGuy = badGuys.begin(); badGuy < badGuys.end(); badGuy++)
	{
		if ((*badGuy)->isAlive)
		{
			(*badGuy)->yDir = 1.0f;
			for (auto title = world.world.begin(); title < world.world.end(); title++)
			{
				(*badGuy)->checkCollisions(title->rect, dt);
			}

			(*badGuy)->move(dt);
			mario.isKilled((*badGuy)->rect, dt);
			if (mario.kills((*badGuy)->rect, dt))
			{
				(*badGuy)->isAlive = false;
				n--;
			}
		}
	}

	badGuys.erase(std::remove_if(badGuys.begin(), badGuys.end(), []( BadGuy* x) {return !( x->isAlive); }), badGuys.end());

	if (nextMairoCount < 0)
	{
		badGuys.push_back(new BadGuy("Characters_Sprites\\Mario & Luigi.png"));
		nextMairoCount = 5.0f;
		n++;
	}

}

void Game::updateFrame()
{
	window.clear(sf::Color::Blue);
	world.draw(window);

	time_text.setString("Time: " + std::to_string(time));
	marionext_text.setString("Next Mario in: " + std::to_string(nextMairoCount));
	
	if (mario.isAlive)
	{
		mario.draw(window);
	}
	else
	{
		gameResult_text.setString("You suck");
	}

	if( n == 0 )
		gameResult_text.setString("You win");
	

	for (auto badGuy = badGuys.begin(); badGuy < badGuys.end(); badGuy++)
	{	
		if ((*badGuy)->isAlive)
		{
			(*badGuy)->draw(window);
		}
	}

	window.draw(time_text);
	window.draw(marionext_text);
	window.draw(gameResult_text);
	window.display();
}

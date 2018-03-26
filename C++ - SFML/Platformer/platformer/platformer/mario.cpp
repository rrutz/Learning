#include "mario.h"
#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>

Mario::Mario()
{
	if (!texture.loadFromFile("Characters_Sprites\\Mario & Luigi.png"))
	{
		std::cout << "Unable to load image" << std::endl;
	}
	else
	{
		// walking right sprites
		for (int i = 0; i < 4; i++)
		{
			sf::Sprite sprite;
			sprite.setTexture(texture);
			sprite.setTextureRect(sf::IntRect(80+17*i, 1, 16, 31));
			sprite.setScale(2.0f, 2.0f);
			sprites.emplace_back( sprite );
		}

		// walking left sprites
		for (int i = 1; i < 4; i++)
		{
			sf::Sprite sprite;
			sprite.setTexture(texture);
			sprite.setTextureRect(sf::IntRect(95+17*i+1, 1, -15, 31));
			sprite.setScale(2.0f, 2.0f);
			sprites.emplace_back( sprite );
		}
	}
}

void Mario::move(float dt)
{
	if (xDir > 0)
	{
		FrameTime -= dt;
		if (FrameTime < 0)
		{
			currentFrame++;
			if(currentFrame >= 4)
			{
				currentFrame = 1;
			}
			FrameTime = 0.05f;
		}
	}
	else if (xDir < 0)
	{
		FrameTime -= dt;
		if (FrameTime < 0)
		{
			currentFrame++;
			if (currentFrame == 7)
			{
				currentFrame = 4;
			}
			FrameTime = 0.05f;
		}
	}
	else 
	{
		currentFrame = 0;
	}

	yVel = 500.0f;
	if(isJumping)
	{
		jumpTime -= dt;
		if (jumpTime < 0)
		{
			isJumping = false;
			jumpTime = 0.3f;
		}
	}
	xPos += xVel * dt*xDir;
	yPos += yVel * dt*yDir;

}

void Mario::jump()
{
	isJumping = true;
	yDir = -1.0f;
}

void Mario::draw(sf::RenderWindow& window)
{
	sprites[currentFrame].setPosition(xPos, yPos);
	window.draw(sprites[currentFrame]);
}

void Mario::checkCollsionY( sf::FloatRect rect)
{
	//std::cout << rect.top;

	sf::FloatRect marioRect = sprites[currentFrame].getGlobalBounds();
	if (marioRect.left + marioRect.width > rect.left  && xPos < rect.left + rect.width)
	{
			
		if (pow((marioRect.top + marioRect.height) - rect.top, 2) < 4.0f)
		{
			yDir = 0.0f;
		}
	}

}

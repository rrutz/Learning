#include "badGuy.h"
#include <string>
#include <SFML/Graphics.hpp>
#include <cmath>
#include <iostream>

BadGuy::BadGuy()
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
			sprite.setTextureRect(sf::IntRect(80 + 17 * i, 1, 16, 31));
			sprite.setScale(2.0f, 2.0f);
			sprites.emplace_back(sprite);
		}

		// walking left sprites
		for (int i = 1; i < 4; i++)
		{
			sf::Sprite sprite;
			sprite.setTexture(texture);
			sprite.setTextureRect(sf::IntRect(95 + 17 * i + 1, 1, -15, 31));
			sprite.setScale(2.0f, 2.0f);
			sprites.emplace_back(sprite);
		}
	}
}

void BadGuy::move(float dt)
{
	if (xDir > 0)
	{
		FrameTime -= dt;
		if (FrameTime < 0)
		{
			currentFrame++;
			if (currentFrame >= 4)
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

	xPos += xVel * dt*xDir;
	yPos += yVel * dt*yDir;

}


void BadGuy::draw(sf::RenderWindow& window)
{
	sprites[currentFrame].setPosition(xPos, yPos);
	window.draw(sprites[currentFrame]);
}

void BadGuy::checkFalling(sf::FloatRect rect)
{
	sf::FloatRect marioRect = sprites[currentFrame].getGlobalBounds();
	if (marioRect.left + marioRect.width > rect.left  && xPos < rect.left + rect.width)
	{
		if (pow((marioRect.top + marioRect.height) - rect.top, 2) < 4.0f)
		{
			yDir = 0.0f;
		}
	}
}


void BadGuy::checkCollsionX(sf::FloatRect rect)
{
	sf::FloatRect marioRect = sprites[currentFrame].getGlobalBounds();

	float marioT = marioRect.top;
	float marioB = marioRect.top + marioRect.height;
	float rectT = rect.top;
	float rectB = rect.top + rect.height;

	if ((marioT < rectT && rectT < marioB) || (marioB > rectB && rectB > marioT) || (marioT > rectT && marioB < rectB))
	{
		if (xDir > 0)
		{
			if (pow((marioRect.left + marioRect.width) - rect.left, 2) < 8.0f)
			{
				xDir = -xDir;
			}
		}
		if (xDir < 0)
		{
			if (pow(marioRect.left - (rect.left + rect.width), 2) < 8.0f)
			{
				xDir = -xDir;
			}
		}

	}
}




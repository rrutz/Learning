#include "characters.h"
#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>

Character::Character( std::string imagePath)
{
	if (!texture.loadFromFile( imagePath ))
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

void Character::walk(float dt)
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

void Character::draw(sf::RenderWindow& window)
{
	sprites[currentFrame].setPosition(xPos, yPos);
	window.draw(sprites[currentFrame]);
}

void Character::checkFalling(sf::FloatRect rect)
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

bool Character::checkCollsionY(sf::FloatRect rect)
{
	sf::FloatRect marioRect = sprites[currentFrame].getGlobalBounds();
	if (marioRect.left + marioRect.width > rect.left  && xPos < rect.left + rect.width)
	{
		if (pow(marioRect.top - (rect.top + rect.height), 2) < 1.0f)
		{
			return true;
		}
	}
	return false;
}

Character::CollisionType Character::checkCollsionX( float xPos_in, float yPos_in, float width_in, float height_in, float dt)
{
	float rectT = yPos_in;
	float rectB = yPos_in + height_in;
	float marioB = yPos + height;

	if ((yPos <= rectT && rectT <= marioB) || (marioB > rectB && rectB > yPos) || (yPos > rectT && marioB < rectB))
	{
		if (xPos + width <= xPos_in && xPos + width + ceil(dt*xVel) > xPos_in)
		{
			return CollisionType::Right;
		}
		if (xPos >= xPos_in + width_in && xPos - ceil(dt*xVel) < xPos_in + width_in)
			return CollisionType::Left;
	}
}


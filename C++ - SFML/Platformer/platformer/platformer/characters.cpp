#include "characters.h"
#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>
#include <iostream>
Character::Character( std::string imagePath, float scale, int pixelWidth, int pixelHeight, float x, float y)
	:
	rect( { x, x + pixelWidth * scale, y, y + pixelHeight * scale, true, true, true, true })
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
			sprite.setTextureRect( sf ::IntRect(80 + (pixelWidth+1) * i, 1, pixelWidth, pixelHeight));
			sprite.setScale(scale, scale);
			sprites.emplace_back(sprite);
		}

		// walking left sprites
		for (int i = 1; i < 4; i++)
		{
			sf::Sprite sprite;
			sprite.setTexture(texture);
			sprite.setTextureRect(sf::IntRect(95 + (pixelWidth + 1) * i, 1, -(pixelWidth-1), pixelHeight));
			sprite.setScale(scale, scale);
			sprites.emplace_back(sprite);
		}
	}
}

void Character::getFrame(float dt)
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
	
}

void Character::move(float dt)
{
	rect.xL += xVel * dt*xDir;
	rect.xR += xVel * dt*xDir;
	rect.yT += yVel * dt*yDir;
	rect.yB += yVel * dt*yDir;
	getFrame(dt);
}

void Character::draw(sf::RenderWindow& window)
{
	sprites[currentFrame].setPosition(rect.xL, rect.yT);
	window.draw(sprites[currentFrame]);
}

void Character::checkFalling(Rect rect_in, float dt)
{
	if (yDir > 0)
	{
		if (rect.CheckTopCollision(rect_in, dt*yVel) )
		{
			yDir = 0.0f;		
		}
	}
}

void Character::checkCollsionY(Rect rect_in, float dt)
{
	if (yDir < 0)
	{
		if (rect.checkBottomCollision(rect_in, dt*yVel))
		{
			yDir = 1.0f;
		}
	}
}



#include "mario.h"
#include <string>
#include <SFML/Graphics.hpp>
#include <iostream>

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

void Mario::move(float dt, int xDir, int yDir)
{
	if (xDir > 0)
	{
		FrameTime--;
		if (FrameTime < 0)
		{
			currentFrame++;
			if(currentFrame >= 4)
			{
				currentFrame = 1;
			}
			FrameTime = 50;
		}
	}
	else if (xDir < 0)
	{
		FrameTime--;
		if (FrameTime < 0)
		{
			currentFrame++;
			if (currentFrame == 7)
			{
				currentFrame = 4;
			}
			FrameTime = 50;
		}
	}
	else 
	{
		currentFrame = 0;
	}

	yVel = 0.0f;
	if (isJumping)
	{
		yDir = 1.0f;
		yVel = -1.3f;
		jumpTime--;
		if (jumpTime < 0)
		{
			isJumping = false;
			jumpTime = 500;
		}
	}
	xPos += xVel * dt*xDir;
	yPos += (yVel+gravity) * dt*yDir;

}

void Mario::jump()
{
	if(yVel ==  0.0f )
		isJumping = true;
}

void Mario::draw(sf::RenderWindow& window)
{
	sprites[currentFrame].setPosition(xPos, yPos);
	window.draw(sprites[currentFrame]);
}

bool Mario::checkCollsionY(float topY)
{
	return(yPos + sprites[0].getTextureRect().height*2> topY);
}

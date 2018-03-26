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
		for (int i = 0; i < 4; i++)
		{
			sf::Sprite sprite;
			sprite.setTexture(texture);
			sprite.setTextureRect(sf::IntRect(80+17*i, 1, 16, 31));
			sprite.setScale(2.0f, 2.0f);
			sprites.emplace_back( sprite );
		}

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

void Mario::move(float dx, float dy)
{
	xPos += dx;
	yPos += dy;

	if (dx > 0)
	{
		holdTime--;
		if (holdTime < 0)
		{
			currentFrame++;
			if(currentFrame >= 4)
			{
				currentFrame = 1;
			}
			holdTime = 50;
		}
	}
	else if (dx < 0)
	{
		holdTime--;
		if (holdTime < 0)
		{
			currentFrame++;
			if (currentFrame == 7)
			{
				currentFrame = 4;
			}
			holdTime = 50;
		}
	}
	else 
	{
		currentFrame = 0;
	}

}

void Mario::jump()
{
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

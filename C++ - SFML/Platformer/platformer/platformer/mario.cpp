#include "mario.h"
#include <SFML/Graphics.hpp>
#include <iostream>


Mario::Mario( std::string imagePath )
	:
	Character( imagePath )
{
	xDir = 0;
	yDir = 0;
	xPos = 50;
	yPos = 50;
}

void Mario::jumping(float dt)
{
	if(isJumping)
	{
		jumpTime -= dt;
		if (jumpTime < 0)
		{
			isJumping = false;
			jumpTime = 0.3f;
			yDir = 1.0f;
		}
	}
}

void Mario::jump()
{
	isJumping = true;
	yDir = -1.0f;
}

void Mario::checkCollsionY2(sf::FloatRect rect)
{
	if (checkCollsionY(rect))
	{
		isJumping = false;
		jumpTime = 0.3f;
	}
}

void Mario::isKilled(float xPos_in, float yPos_in, float width_in, float height_in, float dt)
{
	
	CollisionType collisionType = checkCollsionX( xPos_in,  yPos_in,  width_in,  height_in, dt);
	
	if (collisionType == CollisionType::Left || collisionType == CollisionType::Right)
	{
		xDir = 0;
		isAlive = false;
	}
}

bool Mario::kills(sf::FloatRect rect)
{
	return false;
}

void Mario::checkCollsionX2(float xPos_in, float yPos_in, float width_in, float height_in, float dt)
{
	CollisionType collisionType = checkCollsionX(xPos_in, yPos_in, width_in, height_in, dt);
	if (collisionType == CollisionType::Left && xDir < 0)
	{
		 xPos = xPos_in + width_in ; xDir = 0;
	}
	if (collisionType == CollisionType::Right && xDir > 0)
	{
		xPos = xPos_in - width; xDir = 0;
	}
}



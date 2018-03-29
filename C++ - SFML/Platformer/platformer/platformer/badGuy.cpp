#include "badGuy.h"
#include <SFML/Graphics.hpp>
#include <iostream>

BadGuy::BadGuy(std::string imagePath)
	:
	Character(imagePath)
{
	xDir = 1.0f;
	if (rand() % 2 == 1)
		xDir = 1.0f;
	else
		xDir = -1.0f;
	yDir = 1.0f;
	xPos = 400;
	yPos = 500;
	xVel = rand() % 500+ 200;
}

void BadGuy::checkCollsionX2(float xPos_in, float yPos_in, float width_in, float height_in, float dt)
{
	CollisionType collisionType = checkCollsionX( xPos_in,  yPos_in,  width_in,  height_in, dt);
	if (collisionType == CollisionType::Left && xDir < 0)
	{
		xDir = -xDir;
		xPos = xPos_in + width_in;
	}
	if (collisionType == CollisionType::Right && xDir > 0)
	{
		xDir = -xDir;
		xPos = xPos_in - width;
	}
}



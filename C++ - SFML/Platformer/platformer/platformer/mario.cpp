#include "mario.h"
#include <SFML/Graphics.hpp>
#include <iostream>


Mario::Mario( std::string imagePath )
	:
	Character(imagePath, 2.0f, 16, 31, 100, 400)
{
	yDir = 1.0f;
	xDir = 0;
	yDir = 0;
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

void Mario::checkCollisions(Rect rect_in, float dt_in)
{
	if (rect.checkBottomCollision(rect_in, dt_in*yVel))
	{
		isJumping = false;
		jumpTime = 0.3f;
	}

	checkFalling(rect_in, dt_in);

	if ((xDir > 0 && rect.checkLeftCollision(rect_in, dt_in*xVel)) || (xDir < 0 && rect.checkRightCollision(rect_in, dt_in*xVel)))
	{
		xDir = 0;
	}
}

void Mario::isKilled(Rect rect_in, float dt_in)
{
	if (( rect.checkLeftCollision(rect_in, dt_in*xVel)) || ( rect.checkRightCollision(rect_in, dt_in*xVel)))
	{
		xDir = 0;
		isAlive = false;
	}
}

bool Mario::kills(Rect rect_in, float dt_in)
{
	if (yDir > 0)
	{
		if (rect.CheckTopCollision(rect_in, dt_in*yVel))
		{
			return true;
		}
	}
	return false;
}




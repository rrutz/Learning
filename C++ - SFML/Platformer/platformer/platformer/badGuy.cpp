#include "badGuy.h"
#include <SFML/Graphics.hpp>
#include <iostream>


BadGuy::BadGuy(std::string imagePath)
	:
	Character(imagePath, 2.0f, 16, 31, 500, 500)
{
	if (rand() % 2 == 1)
		xDir = 1.0f;
	else
		xDir = -1.0f;
	yDir = 1.0f;
	xVel = rand() % 400+ 200;
}

void BadGuy::checkCollisions(Rect rect_in, float dt_in)
{
	checkFalling(rect_in, dt_in);
	if ((xDir > 0 && rect.checkLeftCollision(rect_in, dt_in*xVel)) || (xDir < 0 && rect.checkRightCollision(rect_in, dt_in*xVel)))
	{
		xDir = -xDir;
	}
}




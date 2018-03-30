#include "rect.h"
#include <cmath>
#include <iostream>
Rect::Rect(float xL_, float xR, float yT, float yB, bool topSolid, bool bottomSolid, bool leftSolid, bool rightSolid)
	:
	xL(xL_),
	xR( xR) ,
	yT( yT ),
	yB(yB ),
	topSolid(topSolid),
	bottomSolid(bottomSolid),
	leftSolid(leftSolid),
	rightSolid(rightSolid)
{
	
}

bool Rect::checkLeftCollision(Rect rect_in, float dx)
{
	// y doesn't overlap
	if (!((yT <= rect_in.yT && rect_in.yT <= yB) || (yB > rect_in.yB && rect_in.yB > yT) || (yT > rect_in.yT && yB < rect_in.yB)))
		return false;

	// left collison with solid left side
	if (xR <= rect_in.xL)
	{
		if (rect_in.leftSolid)
		{
			if (xR + ceil(dx) > rect_in.xL)
				return true;
		}
	}

	// left collison with solid right side
	if (xR <= rect_in.xR)
	{
		if (rect_in.rightSolid)
		{
			if (xR + ceil(dx) > rect_in.xR)
				return true;
		}
	}

	return false;
}

bool Rect::checkRightCollision(Rect rect_in, float dx)
{
	// y doesn't overlap
	if (!((yT <= rect_in.yT && rect_in.yT <= yB) || (yB > rect_in.yB && rect_in.yB > yT) || (yT > rect_in.yT && yB < rect_in.yB)))
		return false;

	// right collison with solid right side
	if ( xL >= rect_in.xR)
	{
		if (rect_in.rightSolid)
		{
			if (xL - ceil(dx) < rect_in.xR)
				return true;
		}
	}

	// right collison with solid left side
	if (xL >= rect_in.xL)
	{
		if (rect_in.leftSolid)
		{
			if (xL - ceil(dx) < rect_in.xL)
				return true;
		}
	}

	return false;
}

bool Rect::checkBottomCollision(Rect rect_in, float dy)
{
	if( !rect_in.bottomSolid )
		return false;

	if( xR > rect_in.xL  && xL < rect_in.xR )
	{
		if( yT >= rect_in.yB &&  yT - ceil(dy)  < rect_in.yB)
		{
			return true;
		}
	}

	return false;
}

bool Rect::CheckTopCollision(Rect rect_in, float dy)
{
	if(!rect_in.topSolid)
		return false;

	if( xR > rect_in.xL  && xL < rect_in.xR)
	{
		if (yB <= rect_in.yT &&  yB + ceil(dy) > rect_in.yT)
		{
			return true;
		}
	}

	return false;
}

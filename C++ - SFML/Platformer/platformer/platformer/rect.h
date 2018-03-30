#pragma once

class Rect
{
public:
	Rect(float xL, float xR, float yT, float yB, bool topSolid, bool bottomSolid, bool leftSolid, bool rightSolid );
	bool checkLeftCollision(Rect rect_in, float dx);
	bool checkRightCollision(Rect rect_in, float dx);
	bool checkBottomCollision(Rect rect_in, float dy);
	bool CheckTopCollision(Rect rect_in, float dy);


public:
	float xL;
	float xR;
	float yT;
	float yB;
	bool topSolid;
	bool bottomSolid;
	bool leftSolid;
	bool rightSolid;

};
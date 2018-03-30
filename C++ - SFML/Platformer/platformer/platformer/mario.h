#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include "characters.h"

class Mario : public Character
{
public:
	Mario(std::string imagePath );
	void jump();
	void jumping(float dt);
	void checkCollisions(Rect rect_in, float dt_in);
	void isKilled(Rect rect_in, float dt_in);
	bool kills(Rect rect_in, float dt_in);

private:

public:
	bool isJumping = false;

private:
	float jumpTime = 0.3f;
};

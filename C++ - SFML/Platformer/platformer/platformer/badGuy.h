#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include "characters.h"

class BadGuy : public Character
{
public:
	BadGuy(std::string imagePath);
	void checkCollisions(Rect rect, float dt);
};




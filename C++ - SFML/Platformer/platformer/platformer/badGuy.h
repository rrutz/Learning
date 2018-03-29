#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include "characters.h"

class BadGuy : public Character
{
public:
	BadGuy(std::string imagePath);
	void checkCollsionX2(float xPos_in, float yPos_in, float width_in, float height_in, float dt);

private:

public:


private:

};




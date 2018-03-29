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
	void checkCollsionX2(float xPos_in, float yPos_in, float width_in, float height_in, float dt);
	void checkCollsionY2(sf::FloatRect rect);
	void isKilled(float xPos_in, float yPos_in, float width_in, float height_in, float dt);
	bool kills(sf::FloatRect rect);
private:

public:
	bool isJumping = false;

private:
	float jumpTime = 0.3f;
};

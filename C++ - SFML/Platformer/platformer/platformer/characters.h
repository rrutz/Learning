#pragma once
#include <SFML/Graphics.hpp>
#include "rect.h"
#include <vector>
#include <string>

class Character
{
public:
	Character( std::string imagePath, float scale, int pixelWidth, int pixelHeight, float x, float y);
	void getFrame(float dt);
	void move(float dt);
	void draw(sf::RenderWindow& window);
	void checkFalling(Rect rect_in, float dt);
	void checkCollsionY(Rect rect_in, float dt);

protected:
	float xVel = 500.0f;
	float yVel = 500.0f;

public:
	bool isAlive = true;
	float xDir = 0.0f;
	float yDir = 1.0f;
	Rect rect;
	

private:
	float FrameTime = 0.05f;
	int currentFrame = 1;
	std::vector<sf::Sprite> sprites;
	sf::Texture texture;
};


#pragma once
#include <SFML/Graphics.hpp>
#include <vector>


class BadGuy
{
public:
	BadGuy();
	void move(float dt);
	void draw(sf::RenderWindow& window);
	void checkFalling(sf::FloatRect rect);
	void checkCollsionX(sf::FloatRect rect);

private:


public:
	bool isAlive = true;
	float xDir = 1.0f;
	float yDir = 1.0f;
	bool isJumping = false;

private:

	float xPos = std::rand() % 500 + 500;
	float yPos = 100.0f;
	float xVel = 500.0f;
	float yVel = 500.0f;
	float gravity = 600.0f;
	float FrameTime = 0.05f;
	int currentFrame = 1;
	sf::Texture texture;
	std::vector<sf::Sprite> sprites;
};


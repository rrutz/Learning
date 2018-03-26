#pragma once
#include <SFML/Graphics.hpp>
#include <vector>

class Mario
{
public:
	Mario();
	void move(float dt);
	void jump();
	void draw(sf::RenderWindow& window);
	void checkCollsionY( sf::FloatRect rect);

private:


public:
	bool isAlive = true;
	float xDir = 0.0f;
	float yDir = 0.0f;
	bool isJumping = false;

private:
	float xPos = 100.f;
	float yPos = 100.0f;
	float xVel = 500.0f;
	float yVel = 0.0f;
	
	float gravity = 600.0f;
	float jumpTime = 0.3f;
	float FrameTime = 0.05f;
	
	int currentFrame = 1;
	sf::Texture texture;
	std::vector<sf::Sprite> sprites;
};

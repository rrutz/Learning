#pragma once
#include <SFML/Graphics.hpp>
#include <vector>

class Mario
{
public:
	Mario();
	void move(float dt, int xDir, int yDir);
	void jump();
	void draw(sf::RenderWindow& window);
	bool checkCollsionY(float topY);

private:


public:
	bool isAlive = true;

private:
	float xPos = 100.f;
	float yPos = 100.0f;
	float xVel = 0.5f;
	float yVel = 0.0f;
	float gravity = 0.5f;
	float jumpTime = 25;
	float FrameTime = 25;
	bool isJumping = false;
	int currentFrame = 1;
	sf::Texture texture;
	std::vector<sf::Sprite> sprites;
};

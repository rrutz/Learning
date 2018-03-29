#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>

class Character
{
protected:
	enum class CollisionType
	{
		Left,
		Right,
		Top,
		Bottom
	};


public:
	Character( std::string imagePath );
	void walk(float dt);
	void draw(sf::RenderWindow& window);
	void checkFalling(sf::FloatRect rect);
	Character::CollisionType checkCollsionX(float xPos_in, float yPos_in, float width_in, float height_in, float dt);
	bool checkCollsionY(sf::FloatRect rect);

private:

public:
	bool isAlive = true;
	float xDir = 0.0f;
	float yDir = 1.0f;
	std::vector<sf::Sprite> sprites;
	int currentFrame = 1;

public:
	float xPos;
	float yPos;
	float xVel = 500.0f;
	float yVel = 500.0f;
	float width = 32.0f;
	float height = 61.0f;

private:
	float FrameTime = 0.05f;
	
	
	sf::Texture texture;
	

	
};


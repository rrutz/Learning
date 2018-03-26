#pragma once
#include <SFML/Graphics.hpp>
#include <vector>

class Mario
{
public:
	Mario();
	void move( float dx, float dy );
	void jump();
	void draw(sf::RenderWindow& window);
	bool checkCollsionY(float topY);

public:
	float xPos = 100.f;
	float yPos = 100.0f;
	bool isAlive = true;
	int currentFrame = 1;
	float holdTime = 25;
	sf::Texture texture;
	std::vector<sf::Sprite> sprites;
};

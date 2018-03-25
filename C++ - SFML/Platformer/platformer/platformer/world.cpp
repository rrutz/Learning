#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>

class World
{
public:
	World(int height, int width)
		:
		height(height),
		width(width)
	{
		for (int i = 0; i < width / title_width; i++)
		{
			sf::RectangleShape rect(sf::Vector2f(title_width, title_height));
			rect.setFillColor(sf::Color::Green);
			rect.setPosition(i* title_width, height - title_height);
			world.push_back(rect);
		}
	}

	void draw(sf::RenderWindow& window)
	{
		for (auto title = world.begin(); title != world.end(); title++)
		{
			window.draw(*title);
		}
	}
private:
	int title_width = 25;
	int title_height = 25;
	int height;
	int width;
	std::vector<sf::RectangleShape> world;
};
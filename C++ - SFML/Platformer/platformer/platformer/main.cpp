#include <SFML/Graphics.hpp>
#include "world.cpp"
int main()
{
	sf::RenderWindow window(sf::VideoMode(1200, 800), "Kick Ass Game!");
	//sf::CircleShape shape(100.f);
	//shape.setFillColor(sf::Color::Green);

	World world(800, 1200);

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}

		window.clear(sf::Color::Blue);
		world.draw(window);
		window.display();

	}

	return 0;
}
#include <SFML/Graphics.hpp>
#include "world.cpp"
#include "mario.h"


int main()
{
	int pixel_Height = 800;
	int pixel_Width = 1200;
	sf::RenderWindow window(sf::VideoMode(pixel_Width, pixel_Height), "Kick Ass Game!");

	Mario mario = Mario();
	World world(25, 50, pixel_Height, pixel_Width);

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}

		float dx = 0.0f;
		float dy = 0.5f;
		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
		{
			dx = 0.5f;
		}
		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
		{
			dx = -0.5f;
		}
		
		// works but is slow
		for (auto title = world.world.begin(); title < world.world.end(); title++ )
		{
			if ( title->isSolid && mario.checkCollsionY(title->getPosition().y))
			{
				
				dy = 0.0f;
			}
		}
		mario.move(dx, dy);



		window.clear(sf::Color::Blue);
		world.draw(window);
		mario.draw(window);
		window.display();

	}

	return 0;
}
#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>

class Title : public sf::RectangleShape
{
public:
	Title(bool isSolid, sf::Color color, int title_width, int title_height, int xPos, int yPos)
		:
		isSolid(isSolid),
		title_width(title_width),
		title_height(title_height),
		sf::RectangleShape( sf::RectangleShape(sf::Vector2f( title_width, title_height)) )
	{
		setFillColor(color);
		setPosition(xPos, yPos);
		
	}
public:
	float title_width;
	float title_height;
	bool isSolid;
};

class World
{
public:
	World(int nHeight, int nWidth, int pixel_Height, int pixel_Width)
		:
		nHeight( nHeight ),
		nWidth( nWidth ),
		pixel_Height( pixel_Height ),
		pixel_Width( pixel_Width )
	{
		// create ground
		int title_width = pixel_Width / nWidth;
		int title_height = pixel_Height / nHeight;
		for (int i = 0; i <= nWidth; i++)
		{
			for (int j = 1; j <= 3; j++)
			{
				int yPos = pixel_Height - j * title_height;
				int xPos = i * title_width;
				world.push_back(Title(true, sf::Color::Green, title_width, title_height, xPos, yPos ));
			}
		}

		// create bricks
		for (int i = 0; i <= nWidth; i++)
		{
			for (int j = 4; j <= 6; j++)
			{
				int yPos = pixel_Height - j * title_height;
				int xPos = i * title_width;
				
				if (i == 0 || i == 5 || i == 10)
				{
					world.push_back(Title(false, sf::Color::Black, title_width, title_height, xPos, yPos));
				}
				else
				{
					world.push_back(Title(false, sf::Color::Blue, title_width, title_height, xPos, yPos));
				}
			}
		}
	}

	void draw(sf::RenderWindow& window)
	{
		for (auto title = world.begin(); title != world.end(); title++)
		{
			window.draw(*title);
		}
	}

	
	std::vector<Title> world;
private:
	int nHeight;
	int nWidth;
	int pixel_Height;
	int pixel_Width;
	
};
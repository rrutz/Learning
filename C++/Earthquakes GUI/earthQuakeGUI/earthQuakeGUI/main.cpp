#include "earthQuakeGUI.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	earthQuakeGUI w;
	w.show();
	return a.exec();
}

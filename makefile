transformada.txt: fourier datos.txt
	./fourier datos.txt > transformada.txt
fourier: fourier.cpp
	c++ -o fourier fourier.cpp
Python commandline utility to read in an image (black pattern on white background) and generate and STL file that will print as a stamp with the pattern from the image.

Please provide the filename of the image and the file to save the STL to. If the image is big the STL will be very big.

Install requirements with:
	pip -r requirements.txt

Example usage:
	./img2stamp.py shark.png shark.stl

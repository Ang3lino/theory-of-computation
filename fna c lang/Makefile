
FILE = main
GLIB = `pkg-config --cflags --libs glib-2.0` 

comp: ${FILE}.c
	gcc -g3 ${FILE}.c vector.c fna.h ${GLIB} -o o

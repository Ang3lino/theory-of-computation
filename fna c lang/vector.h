#ifndef VECTOR_H
#define VECTOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include <errno.h>

// size_t es un unsigned int
typedef struct vector {
    void **item;
    size_t size;
    size_t capacity; // private
} vector;

// typedef void *T; // Emulacion generica

vector *new_vector (void);

// functional
vector *vfilter(vector *, bool (*)(void *)); 
vector *vflatten(vector *);
vector *vmap(vector *, void *(*)(void *));

void *vat(vector *, const int i);
void *vpop_back (vector *);
void *vpop_front (vector *);

void vresize (vector *, size_t);
void vpush_back (vector *, void *);
void vpush_front (vector *, void *);
void vclear (vector *);
void vresize (vector *, size_t);
void vadd (vector *, size_t, void *);
void vset (vector *, size_t, void *);

#endif
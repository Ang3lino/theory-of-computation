#include "vector.h"

// private:
static void 
resize (vector *v) {
    v->capacity *= 2;
	v->item = realloc(v->item, sizeof(void *) * v->capacity);
    if (v->item == NULL) {
        perror ("Empty memory D: \n");
        exit (EXIT_FAILURE);
    }
}

static void 
moveSubvectorOneStepRight(vector *v, int a) {
	int i;
	for (i = v->size - 1; i >= a; i--)
		v->item[i + 1] = v->item[i];
}

// public:
vector *
vfilter(vector *self, bool (*cmpf)(void *)) {
    vector *other = new_vector();
    int i;
    for (i = 0; i < self->size; i++) {
        if (cmpf(self->item[i])) 
            vpush_back(other, self->item[i]);
    }
    return other;
}

vector * 
vmap(vector *self, void *(*fun)(void *)) {
    vector *other = new_vector();
    int i;
    for (i = 0; i < self->size; i++)
        vpush_back(other, fun(self->item[i]));
    return other;
}

vector * // if a vector has vectors
vflatten(vector *self) {
    vector *solution = new_vector();
    int i, j;
    for (i = 0; i < self->size; i++) {
        vector *current = self->item[i];
        if (current->size > 0) {
            for (j = 0; j < current->size; j++) 
                vpush_back(solution, current->item[i]);
        }
    }
    return solution;
}

void * vat(vector *self, const int i) { return self->item[i]; }

void // b must be greather than a
vinsert(vector *dest, vector *src, const int self_pos, const int a, const int b) {
    int delta = b - a;
    if (dest->size < delta)
        vresize(dest, delta);
    for (int i = a, j = self_pos; i < b; i++, j++)
        vset(dest, j, src->item[j]);
}

vector *
new_vector (void) {
    vector *v = malloc(sizeof(vector));
    v->capacity = 2;
    v->size = 0;
    v->item = calloc (sizeof (void *), v->capacity);
    return v;
}


void 
vpush_back (vector *v, void *data) {
    if (v->size  + 1 >= v->capacity)
        resize (v);
    v->item[v->size++] = data;
}

void 
vpush_front (vector *v, void *data) {
    v->size++;  
	int i;
    if (v->size > v->capacity)
        resize (v);
	moveSubvectorOneStepRight (v, 0);
	v->item[0] = data;
}

// private:
/*
void  // last implementation
vresize (vector *v, size_t len) {
    while (v->capacity < len)
        resize (v);
    v->size = len;
}
*/

void // Se debe hacer que len > 0
vresize (vector *v, size_t len) {
    int i = 0;
    while (i < len)
        i = i << 1;
    v->capacity = i;
    v->size = len;
    v->item = realloc(v->item, sizeof(void *) * v->capacity);
    if (v->item == NULL) {
        perror ("Empty memory D: \n");
        exit (EXIT_FAILURE);
    }
}

void *
vpop_back (vector *v) {
    if (v->size <= 0) {
        perror ("Error at vecpop_back: " 
                "emtpy vector. -_- \n");
        exit (EXIT_FAILURE);
    }
    return v->item[--v->size];
}

void 
vset (vector *v, size_t index, void *data) {
    if (index < v->size && index >= 0) 
        v->item[index] = data;
    else {
        perror ("Error at vec_set: invalid index -_- ");
        exit (EXIT_FAILURE);
    }
}

void  
vadd (vector *v, size_t index, void *data) {
    if (index >= v->size || index < 0) {
        perror ("Error at vec_add: invalid index -_- ");
        exit (EXIT_FAILURE);
    }
	moveSubvectorOneStepRight(v, index);
	v->item[index] = data;
}

void 
vclear(vector *v) {
    free(v->item);
    free(v);
}


#ifndef FNA_H
#define FNA_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include <glib.h>

#include "vector.h"

typedef struct {
    int id;
    GString *symbol;
} dpair; // delta pair

typedef struct { // states and alphatet ignored
    vector *initial_states, *final_states;
    GHashTable *delta;
} fna; // finite nondeterministic automata

static uint _hash(const void *key) {
    dpair *k = ((dpair *) key);
    return k->id + g_string_hash(k->symbol);
}

static int _equals(const void *p, const void *q) { // for compare values
    dpair *a = (dpair *) p;
    dpair *b = (dpair *) q;
    return a->id == b->id && g_string_equal(a->symbol, b->symbol);
    //vector *a = (vector *) p;
    //vector *b = (vector *) q;
    //if (a->size != b->size) return false;
    //else for (int i = 0; i < a->size; i++)
    //    if (a->item[i] != b->item[i]) return false;
    //return true;
}

fna *new_fna(vector *initial_s, vector *final_s) {
    fna *self = malloc(sizeof(fna));
    self->initial_states = initial_s;
    self->final_states = final_s;
    self->delta = g_hash_table_new(_hash, _equals);
    return self;
}

void fna_add(fna *self, dpair *key, int dest) {
    int *destiny = malloc(sizeof(int)); // ALLOCATE FUCKING MEMORY
    *destiny = dest;
    if (g_hash_table_contains((*self).delta, key)) { // get a vector and modify it
        vector *v = (vector *) g_hash_table_lookup((*self).delta, key); // get
        vpush_back(v, destiny); 
        //for (int i = 0; i < v->size; i++)
        //    printf("%d \n", *(int *) v->item[i]);
    } else { 
        vector *bucket = new_vector();
        vpush_back(bucket, destiny);
        g_hash_table_insert((*self).delta, key, bucket);
        vector *w = g_hash_table_lookup((*self).delta, key);
        //for (int i = 0; i < w->size; i++)
        //    printf("%d \n", *(int *) w->item[i]);
    }
}

#endif
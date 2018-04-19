
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

static int _equals(const void *p, const void *q) {
    dpair *a = (dpair *) p;
    dpair *b = (dpair *) q;
    return a->id == b->id && g_string_equal(a->symbol, b->symbol);
}

fna *new_fna(vector *initial_s, vector *final_s) {
    fna *self = malloc(sizeof(fna));
    self->initial_states = initial_s;
    self->final_states = final_s;
    self->delta = g_hash_table_new(_hash, _equals);
    return self;
}

void fna_add(fna *self, const int id, const char *symbol, int destiny) {
    dpair *key = malloc(sizeof(dpair)); // build gpair key
    key->id = id;
    key->symbol = g_string_new(symbol);
    vector *bucket;
    if (g_hash_table_contains(self->delta, key)) {
        bucket = (vector *) g_hash_table_lookup(self->delta, key);
        vpush_back(bucket, &destiny); // warning
    } else { // push a vector direction
        bucket = new_vector();
        vpush_back(bucket, &destiny);
        g_hash_table_insert(self->delta, key, bucket);
    }
    printf("%d \n", *(int *) vat(bucket, 0));
}

#endif
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
#include <glib.h>

#include "vector.h"
#include "fna.h"

char *file_as_string(const char *path) {
    FILE *f = fopen(path, "r+");
    assert(f != NULL);
    char *buffer = 0;   
    fseek (f, 0, SEEK_END);
    long length = ftell (f);
    fseek (f, 0, SEEK_SET);
    buffer = malloc (length);
    assert(buffer != NULL);
    fread (buffer, 1, length, f);
    fclose (f);
    return buffer;
}

size_t strcount(const char *src, const char *str2find) {
    int count = 0;
    while (src = strstr(src, str2find)) {
        count++;
        src++;
    }
    return count;
}

vector *split_line(const char *splitted) {
    uint initial_len = strcount(splitted, ",") + 1;
    char **str_initial = g_strsplit(splitted, ",", -1); // alphabet and states don't matter
    vector *initial = new_vector();
    for (uint i = 0; i < initial_len; i++) {
        int *x = malloc(sizeof(int));
        *x =  atoi(str_initial[i]);
        vpush_back(initial, x);
    }
    return initial;
}

void build_fna_from_file(const char *path) {
    const char *text = file_as_string(path);
    //printf("%s\n", text);
    char **splitted = g_strsplit(text, "\n", -1);
    const uint lines = strcount(text, "\n") + 1;
    //for (uint i = 0; i < lines; i++) {
    //    const char *tmp = splitted[i];
    //    printf("%s\n", tmp);
    //}
    vector *initial = split_line(splitted[2]);
    vector *final = split_line(splitted[3]);
    fna *automata = new_fna(initial, final);
    for (uint i = 4; i < lines; i++) {
        dpair *p = malloc(sizeof(dpair));
        char **current = g_strsplit(splitted[i], ",", -1);
        int id = atoi(current[0]);
        const char *symbol = (current[1]);
        int dest = atoi(current[2]);
        //printf("%d ", p->id);
        //printf("%s ", (char *) p->symbol->str);
        //printf("%d \n", dest);
        fna_add(automata, id, symbol, dest);
        dpair q = { .id = id, .symbol = g_string_new(symbol) };
        vector *v = (vector *) g_hash_table_lookup(automata->delta, &q);
        if (v) {
            for (int j = 0; j < v->size; j++) {
                printf("%d \n", *(int *) vat(v, j));
            }
        }
    }
}

void main(void) {
    build_fna_from_file("test.txt");
}
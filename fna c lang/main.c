#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
#include <glib.h>

#include "vector.h"
#include "fna.h"

char *file_as_string(const char *path) {
    FILE *f = fopen(path, "r");
    assert(f != NULL);
    char *buffer = 0;   
    fseek (f, 0, SEEK_END);
    long length = ftell (f);
    fseek (f, 0, SEEK_SET);
    buffer = malloc (length);
    assert(buffer != NULL);
    fread (buffer, 1, length, f);
    //printf("\n"); // if i don't put this file string gets corrupted ?!
    //fclose (f); // don't close it, if you do so buffer gets corrupted
    //printf("File readed succesfuly\n%s\n", buffer);
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

// returns a vector of integers
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

fna *build_fna_from_file(const char *path) {
    const char *text = file_as_string(path);
    printf("\n%s \n", text);
    char **splitted = g_strsplit(text, "\n", -1); // -1 for all the entire string
    const uint lines = strcount(text, "\n") + 1;
    //for (uint i = 0; i < lines; i++) {
    //    const char *tmp = splitted[i];
    //    printf("%s\n", tmp);
    //}
    vector *initial = split_line(splitted[2]);
    vector *final = split_line(splitted[3]);
    fna *automata = new_fna(initial, final);
    //puts("initial states in automata");
    //for (int i = 0; i < automata->initial_states->size; i++) 
    //    printf("%d  \n", *(int *) automata->initial_states->item[i]);
    //puts("final states in automata");
    //for (int i = 0; i < automata->final_states->size; i++) 
    //    printf("%d  \n", *(int *) automata->final_states->item[i]);
    //puts("-=-=-=-=-=-=-=-=-=-=-=-=-=");
    for (uint i = 4; i < lines; i++) {
        dpair *p = malloc(sizeof(dpair));
        char **current = g_strsplit(splitted[i], ",", -1);
        p->id = atoi(current[0]);
        //printf("%d \n", id);
        p->symbol = g_string_new(current[1]);
        //printf("%s \n", symbol);
        int dest = atoi(current[2]);
        //printf("%d \n", dest);
        //printf("%d ", p->id);
        //printf("%s ", (char *) p->symbol->str);
        //printf("%d \n", dest);
        fna_add(automata, p, dest);
        //vector *v = (vector *) g_hash_table_lookup(automata->delta, p);
        //puts("-=-=-=-=-=-=-=-=-=-=-=-=-=");
        //if (v) {
        //    for (int j = 0; j < v->size; j++) {
        //        printf("%d \n", *(int *) vat(v, j));
        //    }
        //}
    }
    return automata;
}

// similar behavior as cin of c++ limited only by returning a "string"
char *strcin () {
	uint cap = 2, i = 0;
    char *s = calloc(cap, sizeof(char));
    assert(s != NULL);
    char c = 'x';
	while ((c = getchar ()) != ' ') {
        if (c == '\n') break;
        if (i == cap) {
            cap *= 2;
            s = realloc(s, cap * sizeof(char));
        }
		*(s + i) = c;
        i++;
	}
	*(s + i) = '\0';
    return s;
}

// it'll return a printable walk if word is accepted, else return NULL
char *process_str(fna *a, const char *word) {
    int i, j, k, n = strlen(word);
    GString *walk = g_string_new(NULL);
    vector *current = a->initial_states; 
    dpair p;
    for (i = 0; i < n; i++) {
        p.id = *(int *) vat(current, 0);
        char *x = calloc(1, sizeof(char));
        sprintf(x, "%c", word[i]); // needed for pass a char * to g_string_new
        p.symbol = g_string_new(x);
        current = g_hash_table_lookup(a->delta, &p);
        if (current == NULL) // value not found
            return NULL;
        char *tmp = calloc(15, sizeof(char)); // allocate mem to append it
        assert(tmp != NULL);
        sprintf(tmp, "(%d %s) -> %d, ", p.id, p.symbol->str, *(int *) vat(current, 0));
        g_string_append(walk, tmp);
    }
    for (i = 0; i < current->size; i++) { // verify this state belongs to final states
        for (j = 0; j < a->final_states->size; j++) {
            int *x = (int *) vat(current, i), *y = (int *) vat(a->final_states, j);
            if (*x == *y)
                return walk->str;
        }
    }
    return NULL;
}

void main(void) {
    fna *automata = build_fna_from_file("test.txt");
    printf("type a word: ");
    char *input = strcin();
    char *printable = process_str(automata, input);
    if (printable) printf("accepted \n%s \n", printable);
    else puts("unaccepted");
}
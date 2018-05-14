from DirectedGraph import *
from collections import deque
import pdb

__author__ = "Angel Lopez Manriquez"

class Grammar:
    """ G = (N, T, S, P) """
    
    def __init__(self, nont, term, productions, start = 'S', epsilon = chr(949)):
        """ 
            nonterminals: set[string]
            terminals: set[string]
            start: str
            productions: dict[string: set[string]]
            epsilon: str, by default it's really epsilon from greek alphabet """
        self.start = start
        self.productions = productions
        self.nonterminals = nont 
        self.terminals = term
        self.epsilon = epsilon

        self.lang_prod = lambda a, b: { x  + y for x in a for y in b } # language product

    def __str__(self):
        """ method called each time we request to print an instance variable. """
        string = 'nonterminals: '
        for nont in self.nonterminals:
            string += '{}'.format(nont)
        string += '\nterminals: '
        for term in self.terminals:
            string += '{}'.format(term)
        string += '\n'
        for head in self.productions:
            string += '{} --> {}\n'.format(head, ' | '.join(self.productions[head]))
        return string

    def remove_useless_productions(self):
        w = list() # it'll be a list of sets
        w.append(set())
        i = 0
        for t in self.terminals: # loop where find which heads derive a terminal
            for h in self.productions:
                for p in self.productions[h]:
                    if t in p:
                        w[0].add(h)
                        break
        while True: # emulation of do-while
            w.append(set())
            for currentP in w[i]: # find which heads derive w[i]
                for h in self.productions:
                    if h in w[i]: # optimization
                        continue
                    for p in self.productions[h]:
                        if currentP in p:
                            w[i + 1].add(h)
                            break
            #print(w[i + 1])
            w[i + 1] = w[i + 1] | w[i]
            #print(w[i])
            if w[i] == w[i +1]: 
                break # w[i] will be our new nonterminals
            i = i + 1
        useless = self.nonterminals - w[i]
        for u in useless: 
            for h in self.productions:
                to_remove = set() # now we'll remove dead productions
                for p in self.productions[h]:
                    if u in p:
                        to_remove.add(p)
                self.productions[h] = self.productions[h] - to_remove
        self.nonterminals = w[i] # update nonterminals set
        print(self)
        self.remove_unreachables()

    def remove_unreachables(self):
        nont = list(self.start) # it'll be a list of nonterminals
        term = list()
        h = self.start
        for p in self.productions[h]:
            for c in p:
                if c in self.nonterminals:
                    nont.append(c)
                elif c in self.terminals:
                    term.append(c)
        for j in range(1, len(nont)): # note |nont| may change
            for p in self.productions[nont[j]]:
                for c in p:
                    if c in self.nonterminals and (not c in nont):
                        nont.append(c) # append a non-repeated symbol
                    elif c in self.terminals and (not c in term):
                        term.append(c)
        unreachables = self.nonterminals - set(nont)
        for u in unreachables: # remove unreachables
            self.productions.pop(u) # pop returns and destroys an element demanded
        self.nonterminals = set(nont)
        self.terminals = set(term)
        print(self)

    def __determine_which_have_epsilon(self):
        """ returns a list with heads that have rules that have epsilon, it also removes
        a body which has epsilon. """
        def helper(p, have_epsilon):
            for c in p:
                if c == self.epsilon:
                    have_epsilon.add(h)
                    break 
        have_epsilon = set()
        for h in self.productions:
            helper(self.productions[h], have_epsilon)
        for x in have_epsilon:
            self.productions[x].remove(self.epsilon)
        return have_epsilon

    def remove_null_productions(self):
        have_epsilon = self.__determine_which_have_epsilon()
        for e in have_epsilon: # replace ocurrence step by step
            for h in self.productions:
                words = list()
                for p in self.productions[h]:
                    for c in p:
                        if c == e:
                            words += self.__replace_ocurrences(p, c)
                            break
                self.productions[h] |= set(words) # join new rules
        print(self)

    def __replace_ocurrences(self, string, char):
        """ Function called when we find a string which has a char that belongs to
            have_epsilon list, we just concatenate characters neede in for loop. """
        n = string.count(char)
        #pdb.set_trace()
        ocurrences = power_set([ x for x in range(1, n + 1) ]) # to know what to replace
        words = []
        for i in range(1 << n): # length of power set
            j = 0
            tmp = str()
            for c in string:
                if c != char:
                    tmp += c
                elif c == char:
                    j = j + 1
                    if not j in ocurrences[i]:
                        tmp += c
            words.append(tmp)
        print(words)
        return words

    def __print_dict(self, cnf):
        """ It prints a dictionary passed by parameters """
        for key in cnf:
            print('{}: '.format(key))
            for value in cnf[key]:
                print(value)
            print()

def power_set(lista):
    """ returns a list of lists, a power set, from a list given using bit operations. """
    n = len(lista)
    power = []
    for i in range(1 << n):
        power.append(list())
        for j in range(n):
            if i & (1 << j) != 0:
                power[i].append(lista[j]) 
    return power


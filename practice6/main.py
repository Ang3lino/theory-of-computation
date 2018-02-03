from DPDA import DPDA


def add_transitions():
    a = DPDA(3, 0, 2, set('abc'), set('ABCDZ'), 'Z')
    a.add_transition((0, 'a', 'Z'), ('0', 'ZC'))
    a.add_transition((0, 'b', 'Z'), ('0', 'ZD'))
    a.add_transition((0, 'a', 'C'), ('0', 'CA'))
    a.add_transition((0, 'a', 'D'), ('0', 'DA'))
    a.add_transition((0, 'a', 'A'), ('0', 'AA'))
    a.add_transition((0, 'a', 'B'), ('0', 'BA'))
    a.add_transition((0, 'b', 'C'), ('0', 'CB'))
    a.add_transition((0, 'b', 'D'), ('0', 'DB'))
    a.add_transition((0, 'b', 'A'), ('0', 'AB'))
    a.add_transition((0, 'b', 'B'), ('0', 'BB'))
    a.add_transition((0, 'c', 'C'), ('1', 'C'))
    a.add_transition((0, 'c', 'D'), ('1', 'D'))
    a.add_transition((0, 'c', 'A'), ('1', 'A'))
    a.add_transition((0, 'c', 'B'), ('1', 'B'))
    a.add_transition((0, 'c', 'Z'), ('2', 'Z'))
    a.add_transition((1, 'a', 'A'), ('1', chr(949)))
    a.add_transition((1, 'b', 'B'), ('1', chr(949)))
    a.add_transition((1, 'a', 'C'), ('2', chr(949)))
    a.add_transition((1, 'b', 'D'), ('2', chr(949)))
    return a
  
a = add_transitions()
print(a.parse('abacaba'))
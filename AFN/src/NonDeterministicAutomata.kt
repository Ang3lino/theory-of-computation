/* Formally an automata A is defined as (Q, Sigma, delta, q0, F)
   In implementation we're only interested q0 and F in the constructor.
   Delta it'll be defined by a method.
 */

class NonDeterministicAutomata(val initial: HashSet<Int>,
                               val finalStates: HashSet<Int>) {
    val states = HashMap<Int, State>()
    var currentStates = ArrayList<State>() // public temporarily
    val epsilon = "^$"

    override fun toString(): String {
        var str = String()
        for (value in states.values) str += "${value}"
        return str
    }

    fun add(index: Int, values: HashMap<String, HashSet<Int>>) {
        states[index] = State(index, values)
    }

    fun setCurrentStates(ints: HashSet<Int>) {
        states.forEach({ (id, state) -> if (id in ints) currentStates.add(state) })
    }

    fun match(word: String): Boolean {
        setCurrentStates(initial)
        for (i in 0 until word.length) {
            if (!skipEpsilons()) return false
        }
        return true
    }

    fun createStates(ids: HashSet<Int>): HashSet<State> {
        var todo = HashSet<State>()
        states.forEach( { (id, state) -> if (id in ids) todo.add(state) })
        println(todo)
        return todo
    }

    fun skipEpsilons(): Boolean {
        if (currentStates.isEmpty()) return false
        var i = 0
        while (i < currentStates.size) {
            var current = currentStates[i]
            if (current.isDefined(epsilon)) {
                val number = current.numberOfFunctions()
                val nextStates = createStates(current.delta(epsilon)!!)
                if (number == 1)  { // delta defined for epsilon only
                    currentStates.addAll(i, nextStates) // currentStates is composed of STATES
                    currentStates.remove(current)
                } else currentStates.addAll(++i, nextStates)
            } else i++
        }
        return true
    }
}
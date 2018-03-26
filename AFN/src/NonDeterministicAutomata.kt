/* Formally an automata A is defined as (Q, Sigma, delta, q0, F)
   In implementation we're only interested q0 and F in the constructor.
   Delta it'll be defined by a method.
 */

class NonDeterministicAutomata(val initial: HashSet<Int>,
                               val finalStates: HashSet<Int>) {

    override fun toString(): String {
        var str = String()
        for (value in states.values) str += "${value}"
        return str
    }

    fun add(index: Int, values: HashMap<String, HashSet<Int>>) {
        states[index] = State(index, values)
    }

    fun setCurrentStates(ints: HashSet<Int>) { // public temporarily
        states.forEach({ (id, state) -> if (id in ints) currentStates.add(state) })
    }

    var epsilonClosure = HashMap<Int, ArrayList<State>>()
    val states = HashMap<Int, State>()
    var currentStates = ArrayList<State>() // public temporarily
    var statesWithSkippedEpsilon = HashMap<Int, List<State>>() // public temporarily
    var initializeOnce = false

    fun match(word: String): Boolean {
        setCurrentStates(initial)
        if (!initializeOnce) {
            initEpsilonClosure()
            initStatesWithSkippedEpsilon()
            initializeOnce = true
        }
        //currentStates.forEach { println(it) }
        word.forEach { char -> // it's actually a Char, not String type
            var statesBuff = ArrayList<State>()
            currentStates.forEach { statesBuff.addAll(statesWithSkippedEpsilon[it.id]!!.asIterable()) }
            currentStates = ArrayList(statesBuff.distinct())
            println("currentChar = ${char}")
            //currentStates.forEach { println(it) }
            statesBuff.clear()
            currentStates.forEach {
                val others = it.delta(char.toString())
                if (others != null) others.forEach { id -> statesBuff.add(states[id]!!) }
            }
            if (statesBuff.isEmpty()) {
                println("i'm here")
                return false
            }
            currentStates = ArrayList(statesBuff.distinct())
        }
        return currentStates.any { it.id in finalStates }
    }

    fun <T> ArrayList<T>.replace (old: T, newValues: Collection<T>) {
        val i = this.indexOf(old)
        this.remove(old)
        this.addAll(i, newValues)
    }

    fun createStates(ids: HashSet<Int>): HashSet<State> {
        var todo = HashSet<State>()
        states.forEach( { (id, state) -> if (id in ids) todo.add(state) })
        println(todo)
        return todo
    }

    fun initStatesWithSkippedEpsilon() { // initEpsilon should have been executed before
        epsilonClosure.forEach { (id, list) ->
            statesWithSkippedEpsilon[id] = list.filter { !("^$" in it._delta.keys) || (it.numberOfFunctions() > 1) }
        }
    }

    fun initEpsilonClosure() { // public temporarily
        states.keys.forEach {
            var tmp = ArrayList<State>()
            createClosure(it, tmp)
            epsilonClosure[it] = tmp
        }
    }

    fun createClosure(id: Int, buffer: ArrayList<State>) { // public temporarily
        buffer.add(states[id]!!)
        if (states[id]!!.isDefined("")) {
            states[id]!!.delta("")!!.forEach { createClosure(it, buffer) }
        }
    }

}
/* Formally an automata A is defined as (Q, Sigma, delta, q0, F)
   In implementation we're only interested q0 and F in the constructor.
   Delta it'll be defined by a method.
 */

class NonDeterministicAutomata(val initial: HashSet<Int>, val finalStates: HashSet<Int>) {

    private var currentStates = ArrayList<State>() // used in match function
    private var epsilonClosure = HashMap<Int, ArrayList<State>>()
    private var statesWithSkippedEpsilon = HashMap<Int, List<State>>() // we skip most epsilon transition
    private var initializeOnce = false // used for initialize the last two variables once
    val states = HashMap<Int, State>()

    fun <T> ArrayList<T>.replace (old: T, newValues: Collection<T>) { // not used function
        val i = this.indexOf(old)
        this.remove(old)
        this.addAll(i, newValues)
    }

    override fun toString(): String {
        var str = String()
        for (value in states.values) str += "${value}"
        return str
    }

    fun add(index: Int, values: HashMap<String, HashSet<Int>>) {
        states[index] = State(index, values)
    }

    private fun setCurrentStates(ints: HashSet<Int>) {
        states.forEach({ (id, state) -> if (id in ints) currentStates.add(state) })
    }

    fun match(word: String): Boolean {
        setCurrentStates(initial)
        if (!initializeOnce) { initEpsilonClosure(); initStatesWithSkippedEpsilon();  initializeOnce = true }
        word.forEach { char -> // it's actually a Char, not String type
            var statesBuff = ArrayList<State>()
            currentStates.forEach { statesBuff.addAll(statesWithSkippedEpsilon[it.id]!!.asIterable()) }
            currentStates = ArrayList(statesBuff.distinct())
            statesBuff.clear()
            currentStates.forEach {
                val others = it.delta(char.toString())
                if (others != null) others.forEach { id -> statesBuff.add(states[id]!!) }
            }
            if (statesBuff.isEmpty()) return false // we can't keep going with word given
            currentStates = ArrayList(statesBuff.distinct())
        }
        return currentStates.any { it.id in finalStates }
    }

    // helper function for initEpsilonClosure
    private fun createClosure(id: Int, buffer: ArrayList<State>) {
        buffer.add(states[id]!!)
        if (states[id]!!.isDefined("")) {
            states[id]!!.delta("")!!.forEach { createClosure(it, buffer) }
        }
    }

    private fun initEpsilonClosure() {
        states.keys.forEach {
            var tmp = ArrayList<State>()
            createClosure(it, tmp)
            epsilonClosure[it] = tmp
        }
    }

    private fun initStatesWithSkippedEpsilon() { // initEpsilon should have been executed before
        epsilonClosure.forEach { (id, list) ->
            statesWithSkippedEpsilon[id] = list.filter { !("^$" in it._delta.keys) || (it.numberOfFunctions() > 1) }
        }
    }

}
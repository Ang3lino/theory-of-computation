
// object state used in automaton
class State (val id: Int,
             var _delta: HashMap<String, HashSet<Int>> = HashMap()) {

    override fun toString(): String { // method called when trying to print this object
        var str = String()
        for ((key, value) in _delta) str += " Id: $id Regex: $key Codomain: $value "
        return str
    }

    fun isDefined(input: String): Boolean { // exists a value for delta distinct than null ?
        return delta(input) != null
    }

    // yeah, i know there exist getters n setters for kotlin, but they aren't
    // useful for me this time...
    fun add(regex: String, codomain: HashSet<Int>) {
        _delta[regex] = codomain
    }

    fun numberOfFunctions(): Int { // number of domains defined for this state
        return _delta.size
    }

    fun delta(char: String): HashSet<Int>? { // we return null if there's no value for input
        for (key in _delta.keys)
            if (char.matches(key))
                return _delta[key]
        return null
    }

    fun String.matches(regex: String): Boolean { // extension function, same behavior a matches method in java for String
        val regularExpr = Regex(regex)
        return regularExpr.matches(this)
    }

}
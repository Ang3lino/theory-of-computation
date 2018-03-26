
fun initAutomata(): NonDeterministicAutomata {
    val auto = NonDeterministicAutomata(hashSetOf(0), hashSetOf(28))
    auto.add(0, hashMapOf("#" to hashSetOf(1)))
    auto.add(1, hashMapOf("i" to hashSetOf(2)))
    auto.add(2, hashMapOf("n" to hashSetOf(3)))
    auto.add(3, hashMapOf("c" to hashSetOf(4)))
    auto.add(4, hashMapOf("l" to hashSetOf(5)))
    auto.add(5, hashMapOf("u" to hashSetOf(6)))
    auto.add(6, hashMapOf("d" to hashSetOf(7)))
    auto.add(7, hashMapOf("e" to hashSetOf(8)))
    auto.add(8, hashMapOf("^$" to hashSetOf(9, 11))) // ^$ is a regex for an empty string
    auto.add(9, hashMapOf(" " to hashSetOf(10)))
    auto.add(10, hashMapOf("^$" to hashSetOf(11)))
    auto.add(11, hashMapOf("<" to hashSetOf(12)))
    auto.add(12, hashMapOf("^$" to hashSetOf(13, 17, 21))) // empty range
    auto.add(13, hashMapOf("^$" to hashSetOf(14)))
    auto.add(14, hashMapOf("[a-z]" to hashSetOf(15)))
    auto.add(15, hashMapOf("^$" to hashSetOf(16)))
    auto.add(16, hashMapOf("^$" to hashSetOf(25)))
    auto.add(17, hashMapOf("^$" to hashSetOf(18)))
    auto.add(18, hashMapOf("[A-Z]" to hashSetOf(19)))
    auto.add(19, hashMapOf("^$" to hashSetOf(20)))
    auto.add(20, hashMapOf("^$" to hashSetOf(25)))
    auto.add(21, hashMapOf("^$" to hashSetOf(22)))
    auto.add(22, hashMapOf("[0-9]" to hashSetOf(23)))
    auto.add(23, hashMapOf("^$" to hashSetOf(24)))
    auto.add(24, hashMapOf("^$" to hashSetOf(25)))
    auto.add(25, hashMapOf("^$" to hashSetOf(12),
                           "." to hashSetOf(26)))
    auto.add(26, hashMapOf("h" to hashSetOf(27)))
    auto.add(27, hashMapOf(">" to hashSetOf(27)))
    auto.add(28, hashMapOf(" " to hashSetOf())) // empty range
    return auto
}

fun main(args: Array<String>) {
    val auto = initAutomata()
    auto.initEpsilonClosure()
    println(auto.epsilonClosure)
    auto.initStatesWithSkippedEpsilon()
    auto.statesWithSkippedEpsilon.forEach { (id, values) -> println("$id \t $values ") }
}

fun <T> ArrayList<T>.replace (old: T, newValues: Collection<T>) {
    val i = this.indexOf(old)
    this.remove(old)
    this.addAll(i, newValues)
}

fun String.matches(regex: String): Boolean {
    val regularExpr = Regex(regex)
    return regularExpr.matches(this)
}


fun main(args: Array<String>) {
    val auto = NonDeterministicAutomata(hashSetOf(6), hashSetOf(12))
    auto.add(6, hashMapOf("d" to hashSetOf(7)))
    auto.add(7, hashMapOf("e" to hashSetOf(8)))
    auto.add(8, hashMapOf("^$" to hashSetOf(9, 11)))
    auto.add(9, hashMapOf(" " to hashSetOf(10)))
    auto.add(10, hashMapOf("^$" to hashSetOf(11)))
    auto.add(11, hashMapOf("<" to hashSetOf(12)))
    auto.add(12, hashMapOf()) // Rango vacio
    auto.setCurrentStates(hashSetOf(8))
    auto.skipEpsilons()
    println(auto.currentStates)
}

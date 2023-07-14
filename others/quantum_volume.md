## [Quantum Volume](https://pennylane.ai/qml/demos/quantum_volume)

- **LINPACK benchmark**: The task of the supercomputers is to solve a dense system of linear equations, and the metric of interest is the rate at which they perform _floating-point operations (FLOPS)_.

- **Error Rate** for a qubit is defined as probability of undesired change in the qubit state. 
- **State Fidelity** is a measure of the difference between the state we have and the state we would like to have, for any (single or multi qubit) quantum system. _Quantum state tomography_ is a means to characterize the actual state.
- **Gate Fidelity** is a measure of the difference between the operation the gate actually performs and the operation we would like the gate to be performed. In this case, you need _quantum process tomography_.

- Quantum computers can’t be judged based on the number of qubits alone. Present-day devices have a number of limitations, an important one being _gate error rates_. Typically the qubits on a chip are not all connected to each other, so it may not be possible to perform operations on arbitrary pairs of them.

- Roughly, the **Quantum Volume** is a measure of the effective number of qubits a processor has. It is calculated by determining the largest number of qubits on which it can reliably run circuits of a prescribed type. Different quantum computers are tasked with solving the same problem, and the success will be a function of many properties: error rates, qubit connectivity, even the quality of the software stack. A single number won’t tell us everything about a quantum computer, but it does establish a framework for comparing them.

### Designing a benchmark for quantum computers
- To set up a benchmark for a quantum computer we need to decide on a number of things:
    1. A family of circuits with a well-defined structure and variable size.
    2. A set of rules detailing how the circuits can be compiled.
    3. A measure of success for individual circuits.
    4. A measure of success for the family of circuits.
    5. (Optional) An experimental design specifying how the circuits are to be run.

#### The circuits
- Quantum volume relates to the largest square circuit that a quantum processor can run reliably. This benchmark uses random square circuits with a very particular form. Specifically, the circuits consist of $d$ sequential layers acting on $d$ qubits. Each layer consists of two parts: a _random permutation_ of the qubits, followed by _Haar-random SU(4)_ operations performed on neighbouring pairs of qubits.

- These circuits satisfy the criteria in item 1 — they have well-defined structure, and it is clear how they can be scaled to different sizes.

- To compute quantum volume we’re allowed to do essentially anything we’d like to the circuits in order to improve them. This includes optimization, hardware-aware considerations such as qubit placement and routing, and even resynthesis by finding unitaries that are close to the target, but easier to implement on the hardware.

- Both the circuit structure and the compilation highlight how quantum volume is about more than just the number of qubits. The error rates will affect the achievable depth, and the qubit connectivity contributes through the layers of permutations because a very well-connected processor will be able to implement these in fewer steps than a less-connected one. Even the quality of the software and the compiler plays a role here: higher-quality compilers will produce circuits that fit better on the target devices, and will thus produce higher quality results.

#### The measures of success

- The problem used for computing quantum volume is called the _heavy output generation problem_. A distribution that is theorized to fulfill this property is the _distribution of heavy output bit strings_. **Heavy bit strings** are those whose outcome probabilities are above the median of the distribution.

- Each circuit in a circuit family has its own heavy output probability. If our quantum computer is of high quality, then we should expect to see heavy outputs quite often across all the circuits. If it’s of poor quality and everything is totally decohered, we will end up with output probabilities that are roughly all the same, as noise will reduce the probabilities to the uniform distribution.

- **The heavy output generation problem quantifies this** — for our family of random circuits, do we obtain heavy outputs at least 2/3 of the time on average? Furthermore, do we obtain this with high confidence? This is the basis for quantum volume. 

- For item 3 the measure of success for each circuit is how often we obtain heavy outputs when we run the circuit and take a measurement. For item 4 the measure of success for the whole family is whether or not the mean of these probabilities is greater than 2/3 with high confidence.
# %%
# Qiskit's Statevector class provides functionality for defining and manipulating quantum state vectors
from qiskit.quantum_info import Statevector
from numpy import sqrt

u = Statevector([1 / sqrt(2), 1 / sqrt(2)])
v = Statevector([(1 + 2.0j) / 3, -2 / 3])
w = Statevector([1 / 3, 2 / 3])

print("State vectors u, v, and w have been defined.")
display(u.draw("latex"))
display(v.draw("text"))

# check to see if a given vector is a valid quantum state vector
display(u.is_valid())
display(v.is_valid())
display(w.is_valid())

# Simulating measurements using Statevector
v.measure()


# %%
from qiskit.visualization import plot_histogram

statistics = v.sample_counts(1000)
display(statistics)
plot_histogram(statistics)


# %%
from qiskit.quantum_info import Operator

X = Operator([[0, 1], [1, 0]])
Y = Operator([[0, -1.0j], [1.0j, 0]])
Z = Operator([[1, 0], [0, -1]])
H = Operator([[1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]])
S = Operator([[1, 0], [0, 1.0j]])
T = Operator([[1, 0], [0, (1 + 1.0j) / sqrt(2)]])

v = Statevector([1, 0])

v = v.evolve(H)
v = v.evolve(T)
v = v.evolve(H)
v = v.evolve(T)
v = v.evolve(Z)

v.draw("latex")


# %%
from qiskit import QuantumCircuit

circuit = QuantumCircuit(1)

# operations are applied sequentially
circuit.h(0)
circuit.t(0)
circuit.h(0)
circuit.t(0)
circuit.z(0)

circuit.draw()


ket0 = Statevector([1, 0])
v = ket0.evolve(circuit)
v.draw("latex")

statistics = v.sample_counts(4000)
plot_histogram(statistics)


###############################################################
#################### Multiple Systems #########################
###############################################################
# %%
from qiskit.quantum_info import Statevector, Operator

# Tensor products
zero, one = Statevector.from_label("0"), Statevector.from_label("1")
zero.tensor(one)  # returns new `Statevector`(|0⟩⊗|1⟩)

# another example
from numpy import sqrt

plus = Statevector.from_label("+")
i_state = Statevector([1 / sqrt(2), 1j / sqrt(2)])

psi = plus.tensor(i_state)
psi

# Operator class also has a tensor method
X = Operator([[0, 1], [1, 0]])

I = Operator([[1, 0], [0, 1]])

X.tensor(I)

# ^ operator to tensor two operators together
psi.evolve(I ^ X)

# CNOT
CNOT = Operator([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

psi.evolve(CNOT)

# By default, measure measures all qubits in the state vector, but we can provide a list of integers to only measure the qubits at those indices.
# %%
from numpy import sqrt

W = Statevector([0, 1, 1, 0, 1, 0, 0, 0] / sqrt(3))
W
result, new_sv = W.measure([0])  # measure qubit 0
print(f"Measured: {result}\nState after measurement:")
new_sv


###############################################################
#################### Quantum circuits #########################
###############################################################
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# The default names for qubits in Qiskit are q_0, q_1 etc, and q when there is just a single qubit.
# QuantumRegister can be used to choose our own names.

X = QuantumRegister(1, "x")
Y = QuantumRegister(1, "y")
A = ClassicalRegister(1, "a")
B = ClassicalRegister(1, "b")
circuit = QuantumCircuit(Y, X, B, A)
circuit.h(Y)
circuit.cx(Y, X)

circuit.measure(Y, B)
circuit.measure(X, A)
circuit.draw()

from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

simulator = AerSimulator()
circuit_simulator = simulator.run(transpile(circuit, simulator), shots=1000)
statistics = circuit_simulator.result().get_counts()
plot_histogram(statistics)


## quantum circuit implementation of the teleportation protocol
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qubit = QuantumRegister(1, "Q")
ebit0 = QuantumRegister(1, "A")
ebit1 = QuantumRegister(1, "B")
a = ClassicalRegister(1, "a")
b = ClassicalRegister(1, "b")

protocol = QuantumCircuit(qubit, ebit0, ebit1, a, b)

# Prepare ebit used for teleportation
protocol.h(ebit0)
protocol.cx(ebit0, ebit1)
protocol.barrier()
# The barrier function creates a visual separation making the circuit diagram more readable, and
# it also prevents Qiskit from performing various simplifications and
# optimizations across barriers during compilation when circuits are run on real hardware.

# Alice's operations
protocol.cx(qubit, ebit0)
protocol.h(qubit)
protocol.barrier()

# Alice measures and sends classical bits to Bob
protocol.measure(ebit0, a)
protocol.measure(qubit, b)
protocol.barrier()

# Bob uses the classical bits to conditionally apply gates
with protocol.if_test((a, 1)):
    protocol.x(ebit1)
with protocol.if_test((b, 1)):
    protocol.z(ebit1)
# if_test function applies an operation conditionally depending on a classical bit or register
protocol.draw()

##################################################################
##################################################################
# Create a new circuit including the same bits and qubits used in the
# teleportation protocol, along with a new "auxiliary" qubit R.
aux = QuantumRegister(1, "R")
test = QuantumCircuit(aux, qubit, ebit0, ebit1, a, b)

# Entangle Q with R
test.h(aux)
test.cx(aux, qubit)
test.barrier()

# Append the protocol the circuit. The 'qubits' argument tells Qiskit that
# the protocol should operate on the qubits numbered 1, 2, and 3 (skipping
# qubit 0, which is R).
test = test.compose(protocol, qubits=[1, 2, 3])
test.barrier()

# After the protocol runs, check that (B,R) is in a phi+ state. We can add
# a new classical bit to the circuit to do this.
test.cx(aux, ebit1)
test.h(aux)
result = ClassicalRegister(1, "Test result")
test.add_register(result)
test.measure(aux, result)

test.draw()

# let's run the Aer simulator on this circuit and plot a histogram of the outputs
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

counts = AerSimulator().run(test).result().get_counts()
plot_histogram(counts)


# filter the counts to focus just on the test result qubit
filtered_counts = {"0": 0, "1": 0}

for result, frequency in counts.items():
    filtered_counts[result[0]] += frequency

plot_histogram(filtered_counts)


#################################################################################
# implementation of superdense coding
#################################################################################
a = "1"
b = "0"

from qiskit import QuantumCircuit

protocol = QuantumCircuit(2)

# Prepare ebit used for superdense coding
protocol.h(0)
protocol.cx(0, 1)
protocol.barrier()

# Alice's operations

if b == "1":
    protocol.z(0)
if a == "1":
    protocol.x(0)
protocol.barrier()

# Bob's actions
protocol.cx(0, 1)
protocol.h(0)
protocol.measure_all()
# measure_all function measures all of the qubits and puts the results into a single classical register

protocol.draw()


from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

counts = AerSimulator().run(protocol).result().get_counts()
for outcome, frequency in counts.items():
    print(f"Measured {outcome} with frequency {frequency}")
plot_histogram(counts)


from qiskit import QuantumCircuit

rbg = QuantumRegister(1, "randomizer")
ebit0 = QuantumRegister(1, "A")
ebit1 = QuantumRegister(1, "B")

Alice_a = ClassicalRegister(1, "Alice a")
Alice_b = ClassicalRegister(1, "Alice b")

test = QuantumCircuit(rbg, ebit0, ebit1, Alice_b, Alice_a)

# Initialize the ebit
test.h(ebit0)
test.cx(ebit0, ebit1)
test.barrier()

# Use the 'randomizer' qubit twice to generate Alice's bits a and b.
test.h(rbg)
test.measure(rbg, Alice_a)
test.h(rbg)
test.measure(rbg, Alice_b)
test.barrier()

# Now the protocol runs, starting with Alice's actions, which depend
# on her bits.
with test.if_test((Alice_b, 1), label="Z"):
    test.z(ebit0)
with test.if_test((Alice_a, 1), label="X"):
    test.x(ebit0)
test.barrier()

# Bob's actions
test.cx(ebit0, ebit1)
test.h(ebit0)
test.barrier()

Bob_a = ClassicalRegister(1, "Bob a")
Bob_b = ClassicalRegister(1, "Bob b")
test.add_register(Bob_b)
test.add_register(Bob_a)
test.measure(ebit1, Bob_a)
test.measure(ebit0, Bob_b)

test.draw()

from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

counts = AerSimulator().run(test).result().get_counts()
plot_histogram(counts)

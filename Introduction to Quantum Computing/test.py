# %%
#!pip install qiskit
# !pip install pylatexenc

# %%
from qiskit import QuantumCircuit

qc = QuantumCircuit(3, 3)
qc.draw(output="mpl")

# %%
qc.measure([0, 1, 2], [0, 1, 2])
qc.draw()

# %%

from qiskit.providers.aer import AerSimulator

sim = AerSimulator()  # make new simulator object
job = sim.run(qc)  # run the experiment
result = job.result()  # get the results
result.get_counts()

# %%
# Create quantum circuit with 3 qubits and 3 classical bits:
qc = QuantumCircuit(3, 3)
qc.x([0, 1])  # Perform X-gates on qubits 0 & 1
qc.measure([0, 1, 2], [0, 1, 2])
qc.draw()  # returns a drawing of the circuit


# %%
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)

# This calculates what the state vector of our qubits would be
# after passing through the circuit 'qc'
ket = Statevector(qc)

# The code below writes down the state vector.
# Since it's the last line in the cell, the cell will display it as output
ket.draw(output="latex")

# qc.cx(1, 0)

# ket = Statevector(qc)
# ket.draw(output="latex")

qc.x(1)
ket = Statevector(qc)
ket.draw(output="latex")


# Let's create a fresh quantum circuit to create Entanglement
qc = QuantumCircuit(2)

qc.h(1)

ket = Statevector(qc)
ket.draw(output="latex")

qc.cx(1, 0)

ket = Statevector(qc)
ket.draw(output="latex")


# %%
from hello_qiskit import run_puzzle

puzzle = run_puzzle(0)
# %%

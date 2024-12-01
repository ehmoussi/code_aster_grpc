"""Partial zzzz503a test case of code_aster."""

from pathlib import Path

from astergrpc_python.client import code_aster
from interfaces.python.code_aster_pb2 import (
    DisplacementReal,
    Elas,
    Material,
    Modelings,
    Physics,
    PressureReal,
)

aster = code_aster()
# mesh
mesh = aster.Mesh()
mesh.readMedFile("zzzz503a.mmed")
# model
model = aster.Model(mesh)
model.addModelingOnMesh(Physics.Mechanics, Modelings.Tridimensional)
model.build()
# material
YOUNG = 200000.0
POISSON = 0.3
Kinv = 3.2841e-4
Kv = 1.0 / Kinv
SY = 437.0
Rinf = 758.0
Qzer = 758.0 - 437.0
Qinf = Qzer + 100.0
b = 2.3
C1inf = 63767.0 / 2.0
C2inf = 63767.0 / 2.0
Gam1 = 341.0
Gam2 = 341.0
C_Pa = 1.0e6
acier = Material(elas=Elas(e=YOUNG, nu=POISSON))
material_field = aster.MaterialField(mesh)
material_field.addMaterialOnMesh(acier)
material_field.build()
# Loads
# - Displacement
displacement = DisplacementReal(Dx=0.0, Dy=0.0, Dz=0.0, nameOfGroup="Bas")
load_1 = aster.ImposedDisplacementReal(model)
load_1.setValue(displacement)
load_1.build()
# - Pressure
pressure = PressureReal(Pres=1000.0, nameOfGroup="Haut")
load_2 = aster.DistributedPressureReal(model)
load_2.setValue(pressure)
load_2.build()
# Physical Problem
study = aster.PhysicalProblem(model, material_field)
study.addLoad(load_1)
study.addLoad(load_2)
study.computeDOFNumbering()
# Discrete Computation
discrete_computation = aster.DiscreteComputation(study)
forces = discrete_computation.getNeumannForces()
elementary_stiffness_matrix = discrete_computation.getLinearStiffnessMatrix(with_dual=False)
elementary_dual_stiffness_matrix = discrete_computation.getDualStiffnessMatrix()
# DOF Numbering
dof_numbering = aster.DOFNumbering()
dof_numbering.computeNumbering((elementary_stiffness_matrix, elementary_dual_stiffness_matrix))
# Assembly Matrix
assembly_matrix = aster.AssemblyMatrixDisplacementReal()
assembly_matrix.addElementaryMatrix(elementary_stiffness_matrix)
assembly_matrix.addElementaryMatrix(elementary_dual_stiffness_matrix)
assembly_matrix.setDOFNumbering(dof_numbering)
assembly_matrix.assemble()
# solver
solver = aster.MumpsSolver()
solver.factorize(assembly_matrix)
result = solver.solve(forces)
result.printMedFile(Path("zzzz503a.rmed"))

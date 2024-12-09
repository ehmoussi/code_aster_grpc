import threading
from pathlib import Path

import grpc
from google.protobuf.empty_pb2 import Empty

from interfaces.python import code_aster_pb2_grpc
from interfaces.python.code_aster_pb2 import (
    DisplacementReal,
    DisplacementRealWithLoadId,
    ElementaryMatrices,
    ElementaryMatrix,
    FieldOnNodesId,
    Material,
    MechanicalLoadReal,
    MedFile,
    Modeling,
    Modelings,
    NeumannForcesParams,
    Physics,
    PressureReal,
    PressureRealWithLoadId,
)


class FieldOnNodes:
    def __init__(self, field_id, channel) -> None:
        self.stub = code_aster_pb2_grpc.FieldOnNodesStub(channel)
        self.field_id = field_id

    def printMedFile(self, filepath: Path) -> None:
        if filepath.is_dir():
            raise ValueError("Can't write into a directory")
        med_file = self.stub.printMedFile(FieldOnNodesId(id=self.field_id))
        with open(filepath, "wb") as f:
            f.write(med_file.content)


class MumpsSolver:
    def __init__(self, channel) -> None:
        self._channel = channel
        self.stub = code_aster_pb2_grpc.MumpsSolverStub(channel)

    def factorize(self, assembly_matrix):
        self.stub.factorize(Empty())

    def solve(self, field: FieldOnNodes) -> FieldOnNodes:
        field_id = self.stub.solve(FieldOnNodesId(id=field.field_id))
        return FieldOnNodes(field_id.id, self._channel)


class AssemblyMatrixDisplacementReal:
    def __init__(self, channel) -> None:
        self.stub = code_aster_pb2_grpc.AssemblyMatrixDisplacementRealStub(channel)

    def addElementaryMatrix(self, elementary_matrix):
        self.stub.addElementaryMatrix(elementary_matrix)

    def setDOFNumbering(self, dof_numbering):
        self.stub.setDOFNumbering(Empty())

    def assemble(self):
        self.stub.assemble(Empty())


class DOFNumbering:
    def __init__(self, channel) -> None:
        self.stub = code_aster_pb2_grpc.DOFNumberingStub(channel)

    def computeNumbering(self, matrices) -> None:
        elementary_matrices = ElementaryMatrices(matrices=matrices)
        # for matrix in matrices:
        #     elementary_matrices.matrices.add(id=matrix.id)
        self.stub.computeNumbering(elementary_matrices)


class DiscreteComputation:
    def __init__(self, aster: "code_aster", channel) -> None:
        self._channel = channel
        self._aster = aster
        self.stub = code_aster_pb2_grpc.DiscreteComputationStub(channel)

    def getNeumannForces(self, time_curr=0.0, time_step=0.0, theta=1, mode=0) -> FieldOnNodes:
        params = NeumannForcesParams(
            time_curr=time_curr, time_step=time_step, theta=theta, mode=mode
        )
        field_on_nodes_id = self.stub.getNeumannForces(params)
        return FieldOnNodes(field_on_nodes_id.id, self._channel)

    def getLinearStiffnessMatrix(self, with_dual=True) -> ElementaryMatrix:
        return self.stub.getLinearStiffnessMatrix(Empty())

    def getDualStiffnessMatrix(self) -> ElementaryMatrix:
        return self.stub.getDualStiffnessMatrix(Empty())


class PhysicalProblem:
    def __init__(self, channel) -> None:
        self.stub = code_aster_pb2_grpc.PhysicalProblemStub(channel)

    def addLoad(self, load) -> None:
        self.stub.addLoad(MechanicalLoadReal(id=load.load.id))

    def computeDOFNumbering(self) -> None:
        self.stub.computeDOFNumbering(Empty())


class ImposedDisplacementReal:
    def __init__(self, channel, load) -> None:
        self.stub = code_aster_pb2_grpc.ImposedDisplacementRealStub(channel)
        self.load = load

    def setValue(self, displacement: DisplacementReal):
        displacement_with_id = DisplacementRealWithLoadId(
            id=self.load.id, displacement=displacement
        )
        self.stub.setValue(displacement_with_id)

    def build(self):
        self.stub.build(self.load)


class DistributedPressureReal:
    def __init__(self, channel, load) -> None:
        self.stub = code_aster_pb2_grpc.DistributedPressureRealStub(channel)
        self.load = load

    def setValue(self, pressure: PressureReal):
        pressure_with_id = PressureRealWithLoadId(id=self.load.id, pressure=pressure)
        self.stub.setValue(pressure_with_id)

    def build(self):
        self.stub.build(self.load)


class MaterialField:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.stub = code_aster_pb2_grpc.MaterialFieldStub(channel)

    def addMaterialOnMesh(self, material: Material) -> None:
        self.stub.addMaterialOnMesh(material)

    def build(self):
        self.stub.build(Empty())


class Model:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.stub = code_aster_pb2_grpc.ModelStub(channel)

    def addModelingOnMesh(self, physics: Physics, modelings: Modelings):
        self.stub.addModelingOnMesh(
            Modeling(
                physics=physics,
                modelings=modelings,
            )
        )

    def build(self):
        self.stub.build(Empty())


class Mesh:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.stub = code_aster_pb2_grpc.MeshStub(channel)

    def readMedFile(self, filepath):
        filepath = Path(filepath)
        med_file = MedFile(
            filename=filepath.name,
            content=filepath.read_bytes(),
        )
        self.stub.readMedFile(med_file)


def stream_logs(stub):
    print("start streaming logs")
    for log_line in stub.StreamLog(Empty()):
        print(f"{log_line.line}")


class code_aster:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = code_aster_pb2_grpc.code_asterStub(self.channel)
        # Start the log streaming in a separate thread
        self.stream_thread = threading.Thread(
            target=stream_logs,
            args=[self.stub],
            daemon=True,
        )
        self.stream_thread.start()
        self.stub.init(Empty())
        self.mesh = None
        self.model = None
        self.loads = {}
        self.neumann_forces = None
        self.stiffness_matrix = None
        self.dual_stiffness_matrix = None

    def Mesh(self) -> Mesh:
        self.stub.Mesh(Empty())
        self.mesh = Mesh(self.channel)
        return self.mesh

    def Model(self, mesh: Mesh) -> Model:
        self.stub.Model(Empty())
        self.model = Model(self.channel)
        return self.model

    def MaterialField(self, mesh: Mesh) -> MaterialField:
        self.stub.MaterialField(Empty())
        self.material_field = MaterialField(self.channel)
        return self.material_field

    def ImposedDisplacementReal(self, model: Model) -> ImposedDisplacementReal:
        load_client = self.stub.ImposedDisplacementReal(Empty())
        load = ImposedDisplacementReal(self.channel, load_client)
        self.loads[load_client.id] = load
        return load

    def DistributedPressureReal(self, model: Model) -> DistributedPressureReal:
        load_client = self.stub.DistributedPressureReal(Empty())
        load = DistributedPressureReal(self.channel, load_client)
        self.loads[load_client.id] = load
        return load

    def PhysicalProblem(self, model: Model, material_field: MaterialField) -> PhysicalProblem:
        self.stub.PhysicalProblem(Empty())
        return PhysicalProblem(self.channel)

    def DiscreteComputation(self, physical_problem: PhysicalProblem) -> DiscreteComputation:
        self.stub.DiscreteComputation(Empty())
        return DiscreteComputation(self, self.channel)

    def DOFNumbering(self) -> DOFNumbering:
        self.stub.DOFNumbering(Empty())
        return DOFNumbering(self.channel)

    def AssemblyMatrixDisplacementReal(self) -> AssemblyMatrixDisplacementReal:
        self.stub.AssemblyMatrixDisplacementReal(Empty())
        return AssemblyMatrixDisplacementReal(self.channel)

    def MumpsSolver(self) -> MumpsSolver:
        self.stub.MumpsSolver(Empty())
        return MumpsSolver(self.channel)

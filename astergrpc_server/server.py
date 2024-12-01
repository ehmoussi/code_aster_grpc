import tempfile
from concurrent import futures
from pathlib import Path

import code_aster
import grpc
from code_aster.Commands import DEFI_MATERIAU
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
    NeumannForcesParams,
    PressureRealWithLoadId,
)


class CodeAsterServicer(code_aster_pb2_grpc.code_asterServicer):
    def __init__(self) -> None:
        super().__init__()
        self.mesh = None
        self.model = None
        self.material_field = None
        self.loads = {}
        self.physical_problem = None
        self.discrete_computation = None
        self.neumann_forces = None
        self.field_on_nodes = {}
        self.elementary_matrices = {}
        self.dof_numbering = None
        self.assembly_matrix = None
        self.solver = None

    def init(self, request, context):
        code_aster.init()
        return Empty()

    def Mesh(self, request, context):
        self.mesh = code_aster.Mesh()
        return Empty()

    def Model(self, request, context):
        if self.mesh is not None:
            self.model = code_aster.Model(self.mesh)
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Mesh need to be called first",
            )

    def MaterialField(self, request, context):
        if self.mesh is not None:
            self.material_field = code_aster.MaterialField(self.mesh)
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Mesh need to be called first",
            )

    def ImposedDisplacementReal(self, request, context) -> MechanicalLoadReal:
        if self.model is not None:
            load = code_aster.ImposedDisplacementReal(self.model)
            load_id = id(load)
            self.loads[load_id] = load
            return MechanicalLoadReal(id=load_id)
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )

    def DistributedPressureReal(self, request, context) -> MechanicalLoadReal:
        if self.model is not None:
            load = code_aster.DistributedPressureReal(self.model)
            load_id = id(load)
            self.loads[load_id] = load
            return MechanicalLoadReal(id=load_id)
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )

    def PhysicalProblem(self, request, context):
        if self.model is None:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )
        if self.material_field is None:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )
        self.physical_problem = code_aster.PhysicalProblem(self.model, self.material_field)
        return Empty()

    def DiscreteComputation(self, request, context):
        if self.physical_problem is None:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "PhysicalProblem need to be called first",
            )
        else:
            self.discrete_computation = code_aster.DiscreteComputation(self.physical_problem)
        return Empty()

    def DOFNumbering(self, request: Empty, context):
        self.dof_numbering = code_aster.DOFNumbering()
        return Empty()

    def AssemblyMatrixDisplacementReal(self, request, context):
        self.assembly_matrix = code_aster.AssemblyMatrixDisplacementReal()
        return Empty()

    def MumpsSolver(self, request, context):
        self.solver = code_aster.MumpsSolver()
        return Empty()

    def get_elementary_matrix(self, matrix_id, context):
        if matrix_id in self.elementary_matrices:
            return self.elementary_matrices[matrix_id]
        else:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unknow matrix",
            )

    def get_field_on_nodes(self, field_id, context):
        if field_id in self.field_on_nodes:
            return self.field_on_nodes[field_id]
        else:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unknow field",
            )


class MeshServicer(code_aster_pb2_grpc.MeshServicer):
    def __init__(self, code_aster: CodeAsterServicer):
        self.code_aster = code_aster

    @property
    def mesh(self):
        return self.code_aster.mesh

    def readMedFile(self, request: MedFile, context):
        if self.mesh is not None:
            with open(request.filename, "wb") as f:
                f.write(request.content)
            self.mesh.readMedFile(request.filename)
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Mesh need to be called first",
            )


class ModelServicer(code_aster_pb2_grpc.ModelServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        super().__init__()
        self.code_aster = code_aster

    def addModelingOnMesh(self, request: Modeling, context):
        if self.code_aster.model is not None:
            self.code_aster.model.addModelingOnMesh(
                code_aster.Physics(request.physics),
                code_aster.Modelings(request.modelings),
            )
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )

    def build(self, request, context):
        if self.code_aster.model is not None:
            self.code_aster.model.build()
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "Model need to be called first",
            )


class MaterialFieldServicer(code_aster_pb2_grpc.MaterialFieldServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        super().__init__()
        self.code_aster = code_aster

    def addMaterialOnMesh(self, request: Material, context):
        if self.code_aster.material_field is not None:
            material = DEFI_MATERIAU(
                ELAS=_F(E=request.elas.e, NU=request.elas.nu),
                VISCOCHAB=_F(
                    K=request.viscochab.K,
                    B=request.viscochab.B,
                    MU=request.viscochab.MU,
                    Q_M=request.viscochab.Q_M,
                    Q_0=request.viscochab.Q_0,
                    C1=request.viscochab.C1,
                    C2=request.viscochab.C2,
                    G1_0=request.viscochab.G1_0,
                    G2_0=request.viscochab.G2_0,
                    K_0=request.viscochab.K_0,
                    N=request.viscochab.N,
                    A_K=request.viscochab.A_K,
                ),
            )
            self.code_aster.material_field.addMaterialOnMesh(material)
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "MaterialField need to be called first",
            )

    def build(self, request: Material, context):
        if self.code_aster.material_field is not None:
            self.code_aster.material_field.build()
            return Empty()
        else:
            context.abort(
                grpc.StatusCode.FAILED_PRECONDITION,
                "MaterialField need to be called first",
            )


class ImposedDisplacementRealServicer(code_aster_pb2_grpc.ImposedDisplacementRealServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        super().__init__()
        self.code_aster = code_aster

    def get_load(self, load_id, context):
        try:
            return self.code_aster.loads[load_id]
        except KeyError:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unknow load",
            )

    def setValue(self, request: DisplacementRealWithLoadId, context):
        load = self.get_load(request.id, context)
        displacement = self._create_displacement(request.displacement)
        load.setValue(displacement, request.displacement.nameOfGroup)
        return Empty()

    def build(self, request, context):
        load = self.get_load(request.id, context)
        load.build()
        return Empty()

    def _create_displacement(self, request: DisplacementReal):
        displacement = code_aster.DisplacementReal()
        displacement.setValue(code_aster.PhysicalQuantityComponent.Dx, request.Dx)
        displacement.setValue(code_aster.PhysicalQuantityComponent.Dy, request.Dy)
        displacement.setValue(code_aster.PhysicalQuantityComponent.Dz, request.Dz)
        return displacement


class DistributedPressureRealServicer(code_aster_pb2_grpc.DistributedPressureRealServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        super().__init__()
        self.code_aster = code_aster

    def get_load(self, load_id, context):
        try:
            return self.code_aster.loads[load_id]
        except KeyError:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unknow load",
            )

    def setValue(self, request: PressureRealWithLoadId, context):
        load = self.get_load(request.id, context)
        pressure = code_aster.PressureReal()
        pressure.setValue(code_aster.PhysicalQuantityComponent.Pres, request.pressure.Pres)
        load.setValue(pressure, request.pressure.nameOfGroup)
        return Empty()

    def build(self, request, context):
        load = self.get_load(request.id, context)
        load.build()
        return Empty()


class PhysicalProblemServicer(code_aster_pb2_grpc.PhysicalProblemServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        super().__init__()
        self.code_aster = code_aster

    def get_load(self, load_id, context):
        try:
            return self.code_aster.loads[load_id]
        except KeyError:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unknow load",
            )

    def addLoad(self, request: MechanicalLoadReal, context) -> Empty:
        load = self.get_load(request.id, context)
        if self.code_aster.physical_problem is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The PhysicalProblem does not have been called first.",
            )
        else:
            self.code_aster.physical_problem.addLoad(load)
        return Empty()

    def computeDOFNumbering(self, request, context):
        if self.code_aster.physical_problem is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The physical problem does not have been called first.",
            )
        else:
            self.code_aster.physical_problem.computeDOFNumbering()
        return Empty()


class DiscreteComputationServicer(code_aster_pb2_grpc.DiscreteComputationServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        self.code_aster = code_aster

    def getNeumannForces(self, request: NeumannForcesParams, context):
        if self.code_aster.discrete_computation is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The DiscreteComputation does not have been called first.",
            )
        else:
            field_on_nodes = self.code_aster.discrete_computation.getNeumannForces(
                time_curr=request.time_curr,
                time_step=request.time_step,
                theta=request.theta,
                mode=request.mode,
            )
            field_id = id(field_on_nodes)
            self.code_aster.field_on_nodes[field_id] = field_on_nodes
        return FieldOnNodesId(id=field_id)

    def getLinearStiffnessMatrix(self, request: Empty, context):
        if self.code_aster.discrete_computation is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The DiscreteComputation does not have been called first.",
            )
        else:
            elementary_matrix = self.code_aster.discrete_computation.getLinearStiffnessMatrix(
                with_dual=False
            )
            matrix_id = id(elementary_matrix)
            self.code_aster.elementary_matrices[matrix_id] = elementary_matrix
        return ElementaryMatrix(id=matrix_id)

    def getDualStiffnessMatrix(self, request: Empty, context):
        if self.code_aster.discrete_computation is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The DiscreteComputation does not have been called first.",
            )
        else:
            elementary_matrix = self.code_aster.discrete_computation.getDualStiffnessMatrix()
            matrix_id = id(elementary_matrix)
            self.code_aster.elementary_matrices[matrix_id] = elementary_matrix
        return ElementaryMatrix(id=matrix_id)


class DOFNumberingServicer(code_aster_pb2_grpc.DOFNumberingServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        self.code_aster = code_aster

    def computeNumbering(self, request: ElementaryMatrices, context):
        if self.code_aster.dof_numbering is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The DOFNumbering does not have been called first.",
            )
        else:
            elementary_matrices = []
            for matrix in request.matrices:
                elementary_matrix = self.code_aster.get_elementary_matrix(matrix.id, context)
                elementary_matrices.append(elementary_matrix)
            self.code_aster.dof_numbering.computeNumbering(elementary_matrices)
            return Empty()


class AssemblyMatrixDisplacementRealServicer(
    code_aster_pb2_grpc.AssemblyMatrixDisplacementRealServicer
):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        self.code_aster = code_aster

    def addElementaryMatrix(self, request: ElementaryMatrix, context):
        if self.code_aster.assembly_matrix is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The AssemblyMatrixDisplacementReal does not have been called first.",
            )
        else:
            matrix = self.code_aster.get_elementary_matrix(request.id, context)
            self.code_aster.assembly_matrix.addElementaryMatrix(matrix)
        return Empty()

    def setDOFNumbering(self, request, context):
        if self.code_aster.dof_numbering is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The DOFNumbering does not have been called first.",
            )
        elif self.code_aster.assembly_matrix is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The AssemblyMatrixDisplacementReal does not have been called first.",
            )
        else:
            self.code_aster.assembly_matrix.setDOFNumbering(self.code_aster.dof_numbering)
        return Empty()

    def assemble(self, request, context):
        if self.code_aster.assembly_matrix is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The AssemblyMatrixDisplacementReal does not have been called first.",
            )
        else:
            self.code_aster.assembly_matrix.assemble()
        return Empty()


class MumpsSolverServicer(code_aster_pb2_grpc.MumpsSolverServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        self.code_aster = code_aster

    def factorize(self, request, context):
        if self.code_aster.assembly_matrix is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The AssemblyMatrixDisplacementReal does not have been called first.",
            )
        elif self.code_aster.solver is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The MumpsSolver does not have been called first.",
            )
        else:
            self.code_aster.solver.factorize(self.code_aster.assembly_matrix)
        return Empty()

    def solve(self, request: FieldOnNodesId, context):
        if self.code_aster.solver is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "The MumpsSolver does not have been called first.",
            )
        else:
            force = self.code_aster.get_field_on_nodes(request.id, context)
            disp = self.code_aster.solver.solve(force)
            disp_id = id(disp)
            self.code_aster.field_on_nodes[disp_id] = disp
            return FieldOnNodesId(id=disp_id)


class FieldOnNodesServicer(code_aster_pb2_grpc.FieldOnNodesServicer):
    def __init__(self, code_aster: CodeAsterServicer) -> None:
        self.code_aster = code_aster

    def printMedFile(self, request: FieldOnNodesId, context):
        field = self.code_aster.get_field_on_nodes(request.id, context)
        with tempfile.TemporaryDirectory() as tmpdir:
            med_filepath = Path(tmpdir, "field.med")
            field.printMedFile(str(med_filepath))
            with open(med_filepath, "rb") as f:
                return MedFile(content=f.read())


def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    code_aster_servicer = CodeAsterServicer()
    code_aster_pb2_grpc.add_code_asterServicer_to_server(code_aster_servicer, server)
    mesh_servicer = MeshServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_MeshServicer_to_server(mesh_servicer, server)
    model_servicer = ModelServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_ModelServicer_to_server(model_servicer, server)
    material_field_servicer = MaterialFieldServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_MaterialFieldServicer_to_server(material_field_servicer, server)
    imposed_displacement_servicer = ImposedDisplacementRealServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_ImposedDisplacementRealServicer_to_server(
        imposed_displacement_servicer, server
    )
    distributed_pressure_servicer = DistributedPressureRealServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_DistributedPressureRealServicer_to_server(
        distributed_pressure_servicer, server
    )
    physical_problem_servicer = PhysicalProblemServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_PhysicalProblemServicer_to_server(
        physical_problem_servicer, server
    )
    discrete_computation_servicer = DiscreteComputationServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_DiscreteComputationServicer_to_server(
        discrete_computation_servicer, server
    )
    dof_numbering_servicer = DOFNumberingServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_DOFNumberingServicer_to_server(dof_numbering_servicer, server)
    assembly_matrix_servicer = AssemblyMatrixDisplacementRealServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_AssemblyMatrixDisplacementRealServicer_to_server(
        assembly_matrix_servicer, server
    )
    mumps_solver_servicer = MumpsSolverServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_MumpsSolverServicer_to_server(mumps_solver_servicer, server)
    field_on_nodes_servicer = FieldOnNodesServicer(code_aster_servicer)
    code_aster_pb2_grpc.add_FieldOnNodesServicer_to_server(field_on_nodes_servicer, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

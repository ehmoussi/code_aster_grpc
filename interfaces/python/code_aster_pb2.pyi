from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Physics(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Mechanics: _ClassVar[Physics]
    Thermal: _ClassVar[Physics]
    Acoustic: _ClassVar[Physics]

class Modelings(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Axisymmetrical: _ClassVar[Modelings]
    DKT: _ClassVar[Modelings]
    DKTG: _ClassVar[Modelings]
    Planar: _ClassVar[Modelings]
    PlanarBar: _ClassVar[Modelings]
    PlaneStrain: _ClassVar[Modelings]
    PlaneStress: _ClassVar[Modelings]
    Tridimensional: _ClassVar[Modelings]
    TridimensionalAbsorbingBoundary: _ClassVar[Modelings]
Mechanics: Physics
Thermal: Physics
Acoustic: Physics
Axisymmetrical: Modelings
DKT: Modelings
DKTG: Modelings
Planar: Modelings
PlanarBar: Modelings
PlaneStrain: Modelings
PlaneStress: Modelings
Tridimensional: Modelings
TridimensionalAbsorbingBoundary: Modelings

class ElementaryMatrices(_message.Message):
    __slots__ = ("matrices",)
    MATRICES_FIELD_NUMBER: _ClassVar[int]
    matrices: _containers.RepeatedCompositeFieldContainer[ElementaryMatrix]
    def __init__(self, matrices: _Optional[_Iterable[_Union[ElementaryMatrix, _Mapping]]] = ...) -> None: ...

class AssemblyMatrix(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class NeumannForcesParams(_message.Message):
    __slots__ = ("time_curr", "time_step", "theta", "mode")
    TIME_CURR_FIELD_NUMBER: _ClassVar[int]
    TIME_STEP_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    time_curr: float
    time_step: float
    theta: float
    mode: int
    def __init__(self, time_curr: _Optional[float] = ..., time_step: _Optional[float] = ..., theta: _Optional[float] = ..., mode: _Optional[int] = ...) -> None: ...

class ElementaryMatrix(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class FieldOnNodesId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class MechanicalLoadReal(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class PressureRealWithLoadId(_message.Message):
    __slots__ = ("id", "pressure")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_FIELD_NUMBER: _ClassVar[int]
    id: int
    pressure: PressureReal
    def __init__(self, id: _Optional[int] = ..., pressure: _Optional[_Union[PressureReal, _Mapping]] = ...) -> None: ...

class PressureReal(_message.Message):
    __slots__ = ("Pres", "nameOfGroup")
    PRES_FIELD_NUMBER: _ClassVar[int]
    NAMEOFGROUP_FIELD_NUMBER: _ClassVar[int]
    Pres: float
    nameOfGroup: str
    def __init__(self, Pres: _Optional[float] = ..., nameOfGroup: _Optional[str] = ...) -> None: ...

class DisplacementRealWithLoadId(_message.Message):
    __slots__ = ("id", "displacement")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    id: int
    displacement: DisplacementReal
    def __init__(self, id: _Optional[int] = ..., displacement: _Optional[_Union[DisplacementReal, _Mapping]] = ...) -> None: ...

class DisplacementReal(_message.Message):
    __slots__ = ("Dx", "Dy", "Dz", "nameOfGroup")
    DX_FIELD_NUMBER: _ClassVar[int]
    DY_FIELD_NUMBER: _ClassVar[int]
    DZ_FIELD_NUMBER: _ClassVar[int]
    NAMEOFGROUP_FIELD_NUMBER: _ClassVar[int]
    Dx: float
    Dy: float
    Dz: float
    nameOfGroup: str
    def __init__(self, Dx: _Optional[float] = ..., Dy: _Optional[float] = ..., Dz: _Optional[float] = ..., nameOfGroup: _Optional[str] = ...) -> None: ...

class MedFile(_message.Message):
    __slots__ = ("filename", "content")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content: bytes
    def __init__(self, filename: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class Modeling(_message.Message):
    __slots__ = ("physics", "modelings")
    PHYSICS_FIELD_NUMBER: _ClassVar[int]
    MODELINGS_FIELD_NUMBER: _ClassVar[int]
    physics: Physics
    modelings: Modelings
    def __init__(self, physics: _Optional[_Union[Physics, str]] = ..., modelings: _Optional[_Union[Modelings, str]] = ...) -> None: ...

class Material(_message.Message):
    __slots__ = ("elas", "viscochab")
    ELAS_FIELD_NUMBER: _ClassVar[int]
    VISCOCHAB_FIELD_NUMBER: _ClassVar[int]
    elas: Elas
    viscochab: ViscoChab
    def __init__(self, elas: _Optional[_Union[Elas, _Mapping]] = ..., viscochab: _Optional[_Union[ViscoChab, _Mapping]] = ...) -> None: ...

class Elas(_message.Message):
    __slots__ = ("e", "nu")
    E_FIELD_NUMBER: _ClassVar[int]
    NU_FIELD_NUMBER: _ClassVar[int]
    e: float
    nu: float
    def __init__(self, e: _Optional[float] = ..., nu: _Optional[float] = ...) -> None: ...

class ViscoChab(_message.Message):
    __slots__ = ("K", "B", "MU", "Q_M", "Q_0", "C1", "C2", "G1_0", "G2_0", "K_0", "N", "A_K")
    K_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    MU_FIELD_NUMBER: _ClassVar[int]
    Q_M_FIELD_NUMBER: _ClassVar[int]
    Q_0_FIELD_NUMBER: _ClassVar[int]
    C1_FIELD_NUMBER: _ClassVar[int]
    C2_FIELD_NUMBER: _ClassVar[int]
    G1_0_FIELD_NUMBER: _ClassVar[int]
    G2_0_FIELD_NUMBER: _ClassVar[int]
    K_0_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    A_K_FIELD_NUMBER: _ClassVar[int]
    K: float
    B: float
    MU: float
    Q_M: float
    Q_0: float
    C1: float
    C2: float
    G1_0: float
    G2_0: float
    K_0: float
    N: float
    A_K: float
    def __init__(self, K: _Optional[float] = ..., B: _Optional[float] = ..., MU: _Optional[float] = ..., Q_M: _Optional[float] = ..., Q_0: _Optional[float] = ..., C1: _Optional[float] = ..., C2: _Optional[float] = ..., G1_0: _Optional[float] = ..., G2_0: _Optional[float] = ..., K_0: _Optional[float] = ..., N: _Optional[float] = ..., A_K: _Optional[float] = ...) -> None: ...

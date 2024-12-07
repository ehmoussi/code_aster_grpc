# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: interfaces/python/code_aster.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'interfaces/python/code_aster.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"interfaces/python/code_aster.proto\x1a\x1bgoogle/protobuf/empty.proto\"9\n\x12\x45lementaryMatrices\x12#\n\x08matrices\x18\x01 \x03(\x0b\x32\x11.ElementaryMatrix\"\x1c\n\x0e\x41ssemblyMatrix\x12\n\n\x02id\x18\x01 \x01(\x03\"X\n\x13NeumannForcesParams\x12\x11\n\ttime_curr\x18\x01 \x01(\x01\x12\x11\n\ttime_step\x18\x02 \x01(\x01\x12\r\n\x05theta\x18\x03 \x01(\x01\x12\x0c\n\x04mode\x18\x04 \x01(\x03\"\x1e\n\x10\x45lementaryMatrix\x12\n\n\x02id\x18\x01 \x01(\x03\"\x1c\n\x0e\x46ieldOnNodesId\x12\n\n\x02id\x18\x01 \x01(\x03\" \n\x12MechanicalLoadReal\x12\n\n\x02id\x18\x01 \x01(\x03\"E\n\x16PressureRealWithLoadId\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x1f\n\x08pressure\x18\x02 \x01(\x0b\x32\r.PressureReal\"1\n\x0cPressureReal\x12\x0c\n\x04Pres\x18\x01 \x01(\x01\x12\x13\n\x0bnameOfGroup\x18\x02 \x01(\t\"Q\n\x1a\x44isplacementRealWithLoadId\x12\n\n\x02id\x18\x01 \x01(\x03\x12\'\n\x0c\x64isplacement\x18\x02 \x01(\x0b\x32\x11.DisplacementReal\"K\n\x10\x44isplacementReal\x12\n\n\x02\x44x\x18\x01 \x01(\x01\x12\n\n\x02\x44y\x18\x02 \x01(\x01\x12\n\n\x02\x44z\x18\x03 \x01(\x01\x12\x13\n\x0bnameOfGroup\x18\x04 \x01(\t\",\n\x07MedFile\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"D\n\x08Modeling\x12\x19\n\x07physics\x18\x01 \x01(\x0e\x32\x08.Physics\x12\x1d\n\tmodelings\x18\x02 \x01(\x0e\x32\n.Modelings\">\n\x08Material\x12\x13\n\x04\x65las\x18\x01 \x01(\x0b\x32\x05.Elas\x12\x1d\n\tviscochab\x18\x02 \x01(\x0b\x32\n.ViscoChab\"\x1d\n\x04\x45las\x12\t\n\x01\x65\x18\x01 \x01(\x01\x12\n\n\x02nu\x18\x02 \x01(\x01\"\xa0\x01\n\tViscoChab\x12\t\n\x01K\x18\x01 \x01(\x01\x12\t\n\x01\x42\x18\x02 \x01(\x01\x12\n\n\x02MU\x18\x03 \x01(\x01\x12\x0b\n\x03Q_M\x18\x04 \x01(\x01\x12\x0b\n\x03Q_0\x18\x05 \x01(\x01\x12\n\n\x02\x43\x31\x18\x06 \x01(\x01\x12\n\n\x02\x43\x32\x18\x07 \x01(\x01\x12\x0c\n\x04G1_0\x18\x08 \x01(\x01\x12\x0c\n\x04G2_0\x18\t \x01(\x01\x12\x0b\n\x03K_0\x18\n \x01(\x01\x12\t\n\x01N\x18\x0b \x01(\x01\x12\x0b\n\x03\x41_K\x18\x0c \x01(\x01*3\n\x07Physics\x12\r\n\tMechanics\x10\x00\x12\x0b\n\x07Thermal\x10\x01\x12\x0c\n\x08\x41\x63oustic\x10\x02*\xa8\x01\n\tModelings\x12\x12\n\x0e\x41xisymmetrical\x10\x00\x12\x07\n\x03\x44KT\x10\x06\x12\x08\n\x04\x44KTG\x10\x07\x12\n\n\x06Planar\x10\x03\x12\r\n\tPlanarBar\x10\x08\x12\x0f\n\x0bPlaneStrain\x10\x04\x12\x0f\n\x0bPlaneStress\x10\x05\x12\x12\n\x0eTridimensional\x10\x01\x12#\n\x1fTridimensionalAbsorbingBoundary\x10\x02\x32\xc3\x06\n\ncode_aster\x12\x38\n\x04init\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x38\n\x04Mesh\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x39\n\x05Model\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x41\n\rMaterialField\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x17ImposedDisplacementReal\x12\x16.google.protobuf.Empty\x1a\x13.MechanicalLoadReal\"\x00\x12H\n\x17\x44istributedPressureReal\x12\x16.google.protobuf.Empty\x1a\x13.MechanicalLoadReal\"\x00\x12\x43\n\x0fPhysicalProblem\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\x13\x44iscreteComputation\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12@\n\x0c\x44OFNumbering\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12R\n\x1e\x41ssemblyMatrixDisplacementReal\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12?\n\x0bMumpsSolver\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12J\n\x16SimpleFieldOnNodesReal\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x32\x39\n\x04Mesh\x12\x31\n\x0breadMedFile\x12\x08.MedFile\x1a\x16.google.protobuf.Empty\"\x00\x32|\n\x05Model\x12\x38\n\x11\x61\x64\x64ModelingOnMesh\x12\t.Modeling\x1a\x16.google.protobuf.Empty\"\x00\x12\x39\n\x05\x62uild\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x32\x84\x01\n\rMaterialField\x12\x38\n\x11\x61\x64\x64MaterialOnMesh\x12\t.Material\x1a\x16.google.protobuf.Empty\"\x00\x12\x39\n\x05\x62uild\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x32\x94\x01\n\x17ImposedDisplacementReal\x12\x41\n\x08setValue\x12\x1b.DisplacementRealWithLoadId\x1a\x16.google.protobuf.Empty\"\x00\x12\x36\n\x05\x62uild\x12\x13.MechanicalLoadReal\x1a\x16.google.protobuf.Empty\"\x00\x32\x90\x01\n\x17\x44istributedPressureReal\x12=\n\x08setValue\x12\x17.PressureRealWithLoadId\x1a\x16.google.protobuf.Empty\"\x00\x12\x36\n\x05\x62uild\x12\x13.MechanicalLoadReal\x1a\x16.google.protobuf.Empty\"\x00\x32\x94\x01\n\x0fPhysicalProblem\x12\x38\n\x07\x61\x64\x64Load\x12\x13.MechanicalLoadReal\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\x13\x63omputeDOFNumbering\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x32\xe2\x01\n\x13\x44iscreteComputation\x12;\n\x10getNeumannForces\x12\x14.NeumannForcesParams\x1a\x0f.FieldOnNodesId\"\x00\x12G\n\x18getLinearStiffnessMatrix\x12\x16.google.protobuf.Empty\x1a\x11.ElementaryMatrix\"\x00\x12\x45\n\x16getDualStiffnessMatrix\x12\x16.google.protobuf.Empty\x1a\x11.ElementaryMatrix\"\x00\x32Q\n\x0c\x44OFNumbering\x12\x41\n\x10\x63omputeNumbering\x12\x13.ElementaryMatrices\x1a\x16.google.protobuf.Empty\"\x00\x32\xe7\x01\n\x1e\x41ssemblyMatrixDisplacementReal\x12\x42\n\x13\x61\x64\x64\x45lementaryMatrix\x12\x11.ElementaryMatrix\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\x0fsetDOFNumbering\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12<\n\x08\x61ssemble\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x32y\n\x0bMumpsSolver\x12=\n\tfactorize\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12+\n\x05solve\x12\x0f.FieldOnNodesId\x1a\x0f.FieldOnNodesId\"\x00\x32;\n\x0c\x46ieldOnNodes\x12+\n\x0cprintMedFile\x12\x0f.FieldOnNodesId\x1a\x08.MedFile\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interfaces.python.code_aster_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PHYSICS']._serialized_start=998
  _globals['_PHYSICS']._serialized_end=1049
  _globals['_MODELINGS']._serialized_start=1052
  _globals['_MODELINGS']._serialized_end=1220
  _globals['_ELEMENTARYMATRICES']._serialized_start=67
  _globals['_ELEMENTARYMATRICES']._serialized_end=124
  _globals['_ASSEMBLYMATRIX']._serialized_start=126
  _globals['_ASSEMBLYMATRIX']._serialized_end=154
  _globals['_NEUMANNFORCESPARAMS']._serialized_start=156
  _globals['_NEUMANNFORCESPARAMS']._serialized_end=244
  _globals['_ELEMENTARYMATRIX']._serialized_start=246
  _globals['_ELEMENTARYMATRIX']._serialized_end=276
  _globals['_FIELDONNODESID']._serialized_start=278
  _globals['_FIELDONNODESID']._serialized_end=306
  _globals['_MECHANICALLOADREAL']._serialized_start=308
  _globals['_MECHANICALLOADREAL']._serialized_end=340
  _globals['_PRESSUREREALWITHLOADID']._serialized_start=342
  _globals['_PRESSUREREALWITHLOADID']._serialized_end=411
  _globals['_PRESSUREREAL']._serialized_start=413
  _globals['_PRESSUREREAL']._serialized_end=462
  _globals['_DISPLACEMENTREALWITHLOADID']._serialized_start=464
  _globals['_DISPLACEMENTREALWITHLOADID']._serialized_end=545
  _globals['_DISPLACEMENTREAL']._serialized_start=547
  _globals['_DISPLACEMENTREAL']._serialized_end=622
  _globals['_MEDFILE']._serialized_start=624
  _globals['_MEDFILE']._serialized_end=668
  _globals['_MODELING']._serialized_start=670
  _globals['_MODELING']._serialized_end=738
  _globals['_MATERIAL']._serialized_start=740
  _globals['_MATERIAL']._serialized_end=802
  _globals['_ELAS']._serialized_start=804
  _globals['_ELAS']._serialized_end=833
  _globals['_VISCOCHAB']._serialized_start=836
  _globals['_VISCOCHAB']._serialized_end=996
  _globals['_CODE_ASTER']._serialized_start=1223
  _globals['_CODE_ASTER']._serialized_end=2058
  _globals['_MESH']._serialized_start=2060
  _globals['_MESH']._serialized_end=2117
  _globals['_MODEL']._serialized_start=2119
  _globals['_MODEL']._serialized_end=2243
  _globals['_MATERIALFIELD']._serialized_start=2246
  _globals['_MATERIALFIELD']._serialized_end=2378
  _globals['_IMPOSEDDISPLACEMENTREAL']._serialized_start=2381
  _globals['_IMPOSEDDISPLACEMENTREAL']._serialized_end=2529
  _globals['_DISTRIBUTEDPRESSUREREAL']._serialized_start=2532
  _globals['_DISTRIBUTEDPRESSUREREAL']._serialized_end=2676
  _globals['_PHYSICALPROBLEM']._serialized_start=2679
  _globals['_PHYSICALPROBLEM']._serialized_end=2827
  _globals['_DISCRETECOMPUTATION']._serialized_start=2830
  _globals['_DISCRETECOMPUTATION']._serialized_end=3056
  _globals['_DOFNUMBERING']._serialized_start=3058
  _globals['_DOFNUMBERING']._serialized_end=3139
  _globals['_ASSEMBLYMATRIXDISPLACEMENTREAL']._serialized_start=3142
  _globals['_ASSEMBLYMATRIXDISPLACEMENTREAL']._serialized_end=3373
  _globals['_MUMPSSOLVER']._serialized_start=3375
  _globals['_MUMPSSOLVER']._serialized_end=3496
  _globals['_FIELDONNODES']._serialized_start=3498
  _globals['_FIELDONNODES']._serialized_end=3557
# @@protoc_insertion_point(module_scope)

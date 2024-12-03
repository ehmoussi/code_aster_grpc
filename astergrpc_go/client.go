package client

import (
	aster_pb "astergrpc/interfaces/go"
	"context"
	"log"
	"os"
	"path/filepath"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
)

type CodeAster struct {
	conn   *grpc.ClientConn
	client aster_pb.CodeAsterClient
	ctx    context.Context
	// mesh   *Mesh
}

func NewCodeAster(serverAddress string, ctx context.Context) *CodeAster {
	conn, err := grpc.NewClient(serverAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect to the server: %v", err)
	}
	client := aster_pb.NewCodeAsterClient(conn)
	// Call the Init method of code_aster
	_, err = client.Init(ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("The initialisation of Code Aster failed: %v", err)
	}
	return &CodeAster{
		conn: conn, client: client, ctx: ctx,
	}
}

func (aster *CodeAster) Close() {
	err := aster.conn.Close()
	if err != nil {
		log.Printf("Failed to close the connection: %v", err)
	}
}

func (aster *CodeAster) Mesh() Mesh {
	aster.client.Mesh(aster.ctx, &emptypb.Empty{})
	mesh := NewMesh(aster.conn, aster.ctx)
	// aster.mesh = mesh
	return *mesh
}

func (aster *CodeAster) Model(mesh Mesh) Model {
	aster.client.Model(aster.ctx, &emptypb.Empty{})
	return *NewModel(aster.conn, aster.ctx)
}

func (aster *CodeAster) MaterialField(mesh Mesh) MaterialField {
	aster.client.MaterialField(aster.ctx, &emptypb.Empty{})
	return *NewMaterialField(aster.conn, aster.ctx)
}

func (aster *CodeAster) ImposedDisplacementReal(model Model) ImposedDisplacementReal {
	mechanicalLoad, err := aster.client.ImposedDisplacementReal(aster.ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("Can't create an ImposedDisplacementReal: %v", err)
	}
	load := NewImposedDisplacementReal(aster.conn, aster.ctx, mechanicalLoad)
	return *load
}

func (aster *CodeAster) DistributedPressureReal(model Model) DistributedPressureReal {
	mechanicalLoad, err := aster.client.DistributedPressureReal(aster.ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("Can't create an DistributedPressureReal: %v", err)
	}
	load := NewDistributedPressureReal(aster.conn, aster.ctx, mechanicalLoad)
	return *load
}

func (aster *CodeAster) PhysicalProblem(model Model, materialField MaterialField) PhysicalProblem {
	aster.client.PhysicalProblem(aster.ctx, &emptypb.Empty{})
	return *NewPhysicalProblem(aster.conn, aster.ctx)
}

func (aster *CodeAster) DiscreteComputation() DiscreteComputation {
	aster.client.DiscreteComputation(aster.ctx, &emptypb.Empty{})
	return *NewDiscreteComputation(aster)
}

func (aster *CodeAster) DOFNumbering() DOFNumbering {
	aster.client.DOFNumbering(aster.ctx, &emptypb.Empty{})
	return *NewDOFNumbering(aster.conn, aster.ctx)
}

func (aster *CodeAster) AssemblyMatrixDisplacementReal() AssemblyMatrixDisplacementReal {
	aster.client.AssemblyMatrixDisplacementReal(aster.ctx, &emptypb.Empty{})
	return *NewAssemblyMatrixDisplacementReal(aster.conn, aster.ctx)
}

func (aster *CodeAster) MumpsSolver() MumpsSolver {
	aster.client.MumpsSolver(aster.ctx, &emptypb.Empty{})
	return *NewMumpsSolver(aster.conn, aster.ctx)
}

// Mesh

type Mesh struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.MeshClient
}

func NewMesh(conn *grpc.ClientConn, ctx context.Context) *Mesh {
	return &Mesh{
		conn, ctx, aster_pb.NewMeshClient(conn),
	}
}

func (mesh *Mesh) ReadMedFile(path string) {
	content, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Can't read the given file %s: %v", path, err)
	}
	medFile := aster_pb.MedFile{
		Filename: filepath.Base(path),
		Content:  content,
	}
	_, err = mesh.client.ReadMedFile(mesh.ctx, &medFile)
	if err != nil {
		log.Fatalf("Can't read the med file: %v", err)
	}
}

// Model
type Model struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.ModelClient
}

func NewModel(conn *grpc.ClientConn, ctx context.Context) *Model {
	client := aster_pb.NewModelClient(conn)
	return &Model{
		conn, ctx, client,
	}
}

func (model *Model) AddModelingOnMesh(physics aster_pb.Physics, modelings aster_pb.Modelings) {
	model.client.AddModelingOnMesh(model.ctx, &aster_pb.Modeling{
		Physics:   physics,
		Modelings: modelings,
	})
}

func (model *Model) Build() {
	model.client.Build(model.ctx, &emptypb.Empty{})
}

// MaterialField

type MaterialField struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.MaterialFieldClient
}

func NewMaterialField(conn *grpc.ClientConn, ctx context.Context) *MaterialField {
	return &MaterialField{
		conn, ctx, aster_pb.NewMaterialFieldClient(conn),
	}
}

func (materialField *MaterialField) AddMaterialOnMesh(material *aster_pb.Material) {
	materialField.client.AddMaterialOnMesh(materialField.ctx, material)
}

func (materialField *MaterialField) Build() {
	materialField.client.Build(materialField.ctx, &emptypb.Empty{})
}

// Loads

type MechanicalLoadReal interface {
	GetLoad() *aster_pb.MechanicalLoadReal
}

// - Displacement
type ImposedDisplacementReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.ImposedDisplacementRealClient
	load   *aster_pb.MechanicalLoadReal
}

func NewImposedDisplacementReal(conn *grpc.ClientConn, ctx context.Context, load *aster_pb.MechanicalLoadReal) *ImposedDisplacementReal {
	return &ImposedDisplacementReal{
		conn, ctx, aster_pb.NewImposedDisplacementRealClient(conn), load,
	}
}

func (displacement *ImposedDisplacementReal) SetValue(value *aster_pb.DisplacementReal) {
	displacementId := aster_pb.DisplacementRealWithLoadId{
		Id:           displacement.load.Id,
		Displacement: value,
	}
	displacement.client.SetValue(displacement.ctx, &displacementId)
}

func (displacement *ImposedDisplacementReal) Build() {
	displacement.client.Build(displacement.ctx, displacement.load)
}

func (displacement *ImposedDisplacementReal) GetLoad() *aster_pb.MechanicalLoadReal {
	return displacement.load
}

// - Pressure
type DistributedPressureReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.DistributedPressureRealClient
	load   *aster_pb.MechanicalLoadReal
}

func NewDistributedPressureReal(conn *grpc.ClientConn, ctx context.Context, load *aster_pb.MechanicalLoadReal) *DistributedPressureReal {
	return &DistributedPressureReal{
		conn, ctx, aster_pb.NewDistributedPressureRealClient(conn), load,
	}
}

func (pressure *DistributedPressureReal) SetValue(value *aster_pb.PressureReal) {
	pressureId := aster_pb.PressureRealWithLoadId{
		Id:       pressure.load.Id,
		Pressure: value,
	}
	pressure.client.SetValue(pressure.ctx, &pressureId)
}

func (pressure *DistributedPressureReal) Build() {
	pressure.client.Build(pressure.ctx, pressure.load)
}

func (pressure *DistributedPressureReal) GetLoad() *aster_pb.MechanicalLoadReal {
	return pressure.load
}

// PhysicalProblem
type PhysicalProblem struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.PhysicalProblemClient
}

func NewPhysicalProblem(conn *grpc.ClientConn, ctx context.Context) *PhysicalProblem {
	return &PhysicalProblem{
		conn, ctx, aster_pb.NewPhysicalProblemClient(conn),
	}
}

func (p *PhysicalProblem) AddLoad(load MechanicalLoadReal) {
	p.client.AddLoad(p.ctx, &aster_pb.MechanicalLoadReal{Id: load.GetLoad().Id})
}

func (p *PhysicalProblem) ComputeDOFNumbering() {
	p.client.ComputeDOFNumbering(p.ctx, &emptypb.Empty{})
}

// DiscreteComputation
type DiscreteComputation struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.DiscreteComputationClient
	aster  *CodeAster
}

func NewDiscreteComputation(aster *CodeAster) *DiscreteComputation {
	return &DiscreteComputation{
		aster.conn, aster.ctx, aster_pb.NewDiscreteComputationClient(aster.conn), aster,
	}
}

func (c *DiscreteComputation) GetNeumannForces(timeCurr float64) FieldOnNodes {
	params := aster_pb.NeumannForcesParams{
		TimeCurr: timeCurr, TimeStep: 0.0, Theta: 1.0, Mode: 0,
	}
	fieldId, err := c.client.GetNeumannForces(c.ctx, &params)
	if err != nil {
		log.Fatalf("Failed to get the Neumann Forces: %v", err)
	}
	return *NewFieldOnNodes(fieldId.Id, c.conn, c.ctx)
}

func (c *DiscreteComputation) GetLinearStiffnessMatrix(with_dual bool) *aster_pb.ElementaryMatrix {
	matrix, err := c.client.GetLinearStiffnessMatrix(c.ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("Failed to get the linear stiffness matrix: %v", err)
	}
	return matrix
}

func (c *DiscreteComputation) GetDualStiffnessMatrix(with_dual bool) *aster_pb.ElementaryMatrix {
	matrix, err := c.client.GetDualStiffnessMatrix(c.ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("Failed to get the dual stiffness matrix: %v", err)
	}
	return matrix
}

// DOFNumbering
type DOFNumbering struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.DOFNumberingClient
}

func NewDOFNumbering(conn *grpc.ClientConn, ctx context.Context) *DOFNumbering {
	return &DOFNumbering{
		conn, ctx, aster_pb.NewDOFNumberingClient(conn),
	}
}

func (d *DOFNumbering) ComputeNumbering(matrices []*aster_pb.ElementaryMatrix) {
	elementaryMatrices := aster_pb.ElementaryMatrices{Matrices: matrices}
	d.client.ComputeNumbering(d.ctx, &elementaryMatrices)
}

// AssemblyMatrixDisplacementReal
type AssemblyMatrixDisplacementReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.AssemblyMatrixDisplacementRealClient
}

func NewAssemblyMatrixDisplacementReal(conn *grpc.ClientConn, ctx context.Context) *AssemblyMatrixDisplacementReal {
	return &AssemblyMatrixDisplacementReal{
		conn, ctx, aster_pb.NewAssemblyMatrixDisplacementRealClient(conn),
	}
}

func (a *AssemblyMatrixDisplacementReal) AddElementaryMatrix(elementaryMatrix *aster_pb.ElementaryMatrix) {
	a.client.AddElementaryMatrix(a.ctx, elementaryMatrix)
}

func (a *AssemblyMatrixDisplacementReal) SetDOFNumbering(DOFNumbering) {
	a.client.SetDOFNumbering(a.ctx, &emptypb.Empty{})
}

func (a *AssemblyMatrixDisplacementReal) Assemble() {
	a.client.Assemble(a.ctx, &emptypb.Empty{})
}

// MumpsSolver
type MumpsSolver struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client aster_pb.MumpsSolverClient
}

func NewMumpsSolver(conn *grpc.ClientConn, ctx context.Context) *MumpsSolver {
	return &MumpsSolver{
		conn, ctx, aster_pb.NewMumpsSolverClient(conn),
	}
}

func (s *MumpsSolver) Factorize(AssemblyMatrixDisplacementReal) {
	s.client.Factorize(s.ctx, &emptypb.Empty{})
}

func (s *MumpsSolver) Solve(field FieldOnNodes) FieldOnNodes {
	fieldOnNodesId, err := s.client.Solve(s.ctx, &aster_pb.FieldOnNodesId{Id: field.fieldId})
	if err != nil {
		log.Fatalf("Failed to solve the system: %v", err)
	}
	return *NewFieldOnNodes(fieldOnNodesId.Id, s.conn, s.ctx)
}

// FieldOnNodes
type FieldOnNodes struct {
	conn    *grpc.ClientConn
	ctx     context.Context
	client  aster_pb.FieldOnNodesClient
	fieldId int64
}

func NewFieldOnNodes(fieldId int64, conn *grpc.ClientConn, ctx context.Context) *FieldOnNodes {
	return &FieldOnNodes{
		conn, ctx, aster_pb.NewFieldOnNodesClient(conn), fieldId,
	}
}

func (f *FieldOnNodes) PrintMedFile(path string) {
	fileInfo, err := os.Stat(path)
	if err == nil && fileInfo.IsDir() {
		log.Fatalf("Can't write into a directory: %s", path)
	}
	medFile, err := f.client.PrintMedFile(f.ctx, &aster_pb.FieldOnNodesId{Id: f.fieldId})
	if err != nil {
		log.Fatalf("Failed to write the file: %v", err)
	}
	file, err := os.Create(path)
	if err != nil {
		log.Fatalf("Can't create the file '%s': %v", path, err)
	}
	defer file.Close()
	_, err = file.Write(medFile.Content)
	if err != nil {
		log.Fatalf("Failed to write the file: %v", err)
	}
}

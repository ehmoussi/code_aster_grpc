package main

import (
	pb "astergrpc/interfaces/go/proto"
	"context"
	"log"
	"os"
	"path/filepath"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
)

type CodeAster struct {
	conn   *grpc.ClientConn
	client pb.CodeAsterClient
	ctx    context.Context
	// mesh   *Mesh
}

func NewCodeAster(serverAddress string, ctx context.Context) *CodeAster {
	conn, err := grpc.NewClient(serverAddress, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect to the server: %v", err)
	}
	client := pb.NewCodeAsterClient(conn)
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
	client pb.MeshClient
}

func NewMesh(conn *grpc.ClientConn, ctx context.Context) *Mesh {
	return &Mesh{
		conn, ctx, pb.NewMeshClient(conn),
	}
}

func (mesh *Mesh) readMedFile(path string) {
	content, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Can't read the given file %s: %v", path, err)
	}
	medFile := pb.MedFile{
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
	client pb.ModelClient
}

func NewModel(conn *grpc.ClientConn, ctx context.Context) *Model {
	client := pb.NewModelClient(conn)
	return &Model{
		conn, ctx, client,
	}
}

func (model *Model) addModelingOnMesh(physics pb.Physics, modelings pb.Modelings) {
	model.client.AddModelingOnMesh(model.ctx, &pb.Modeling{
		Physics:   physics,
		Modelings: modelings,
	})
}

func (model *Model) build() {
	model.client.Build(model.ctx, &emptypb.Empty{})
}

// MaterialField

type MaterialField struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.MaterialFieldClient
}

func NewMaterialField(conn *grpc.ClientConn, ctx context.Context) *MaterialField {
	return &MaterialField{
		conn, ctx, pb.NewMaterialFieldClient(conn),
	}
}

func (materialField *MaterialField) addMaterialOnMesh(material *pb.Material) {
	materialField.client.AddMaterialOnMesh(materialField.ctx, material)
}

func (materialField *MaterialField) build() {
	materialField.client.Build(materialField.ctx, &emptypb.Empty{})
}

// Loads

type MechanicalLoadReal interface {
	GetLoad() *pb.MechanicalLoadReal
}

// - Displacement
type ImposedDisplacementReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.ImposedDisplacementRealClient
	load   *pb.MechanicalLoadReal
}

func NewImposedDisplacementReal(conn *grpc.ClientConn, ctx context.Context, load *pb.MechanicalLoadReal) *ImposedDisplacementReal {
	return &ImposedDisplacementReal{
		conn, ctx, pb.NewImposedDisplacementRealClient(conn), load,
	}
}

func (displacement *ImposedDisplacementReal) setValue(value *pb.DisplacementReal) {
	displacementId := pb.DisplacementRealWithLoadId{
		Id:           displacement.load.Id,
		Displacement: value,
	}
	displacement.client.SetValue(displacement.ctx, &displacementId)
}

func (displacement *ImposedDisplacementReal) build() {
	displacement.client.Build(displacement.ctx, displacement.load)
}

func (displacement *ImposedDisplacementReal) GetLoad() *pb.MechanicalLoadReal {
	return displacement.load
}

// - Pressure
type DistributedPressureReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.DistributedPressureRealClient
	load   *pb.MechanicalLoadReal
}

func NewDistributedPressureReal(conn *grpc.ClientConn, ctx context.Context, load *pb.MechanicalLoadReal) *DistributedPressureReal {
	return &DistributedPressureReal{
		conn, ctx, pb.NewDistributedPressureRealClient(conn), load,
	}
}

func (pressure *DistributedPressureReal) setValue(value *pb.PressureReal) {
	pressureId := pb.PressureRealWithLoadId{
		Id:       pressure.load.Id,
		Pressure: value,
	}
	pressure.client.SetValue(pressure.ctx, &pressureId)
}

func (pressure *DistributedPressureReal) build() {
	pressure.client.Build(pressure.ctx, pressure.load)
}

func (pressure *DistributedPressureReal) GetLoad() *pb.MechanicalLoadReal {
	return pressure.load
}

// PhysicalProblem
type PhysicalProblem struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.PhysicalProblemClient
}

func NewPhysicalProblem(conn *grpc.ClientConn, ctx context.Context) *PhysicalProblem {
	return &PhysicalProblem{
		conn, ctx, pb.NewPhysicalProblemClient(conn),
	}
}

func (p *PhysicalProblem) addLoad(load MechanicalLoadReal) {
	p.client.AddLoad(p.ctx, &pb.MechanicalLoadReal{Id: load.GetLoad().Id})
}

func (p *PhysicalProblem) computeDOFNumbering() {
	p.client.ComputeDOFNumbering(p.ctx, &emptypb.Empty{})
}

// DiscreteComputation
type DiscreteComputation struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.DiscreteComputationClient
	aster  *CodeAster
}

func NewDiscreteComputation(aster *CodeAster) *DiscreteComputation {
	return &DiscreteComputation{
		aster.conn, aster.ctx, pb.NewDiscreteComputationClient(aster.conn), aster,
	}
}

func (c *DiscreteComputation) getNeumannForces(timeCurr float64) FieldOnNodes {
	params := pb.NeumannForcesParams{
		TimeCurr: timeCurr, TimeStep: 0.0, Theta: 1.0, Mode: 0,
	}
	fieldId, err := c.client.GetNeumannForces(c.ctx, &params)
	if err != nil {
		log.Fatalf("Failed to get the Neumann Forces: %v", err)
	}
	return *NewFieldOnNodes(fieldId.Id, c.conn, c.ctx)
}

func (c *DiscreteComputation) getLinearStiffnessMatrix(with_dual bool) *pb.ElementaryMatrix {
	matrix, err := c.client.GetLinearStiffnessMatrix(c.ctx, &emptypb.Empty{})
	if err != nil {
		log.Fatalf("Failed to get the linear stiffness matrix: %v", err)
	}
	return matrix
}

func (c *DiscreteComputation) getDualStiffnessMatrix(with_dual bool) *pb.ElementaryMatrix {
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
	client pb.DOFNumberingClient
}

func NewDOFNumbering(conn *grpc.ClientConn, ctx context.Context) *DOFNumbering {
	return &DOFNumbering{
		conn, ctx, pb.NewDOFNumberingClient(conn),
	}
}

func (d *DOFNumbering) computeNumbering(matrices []*pb.ElementaryMatrix) {
	elementaryMatrices := pb.ElementaryMatrices{Matrices: matrices}
	d.client.ComputeNumbering(d.ctx, &elementaryMatrices)
}

// AssemblyMatrixDisplacementReal
type AssemblyMatrixDisplacementReal struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.AssemblyMatrixDisplacementRealClient
}

func NewAssemblyMatrixDisplacementReal(conn *grpc.ClientConn, ctx context.Context) *AssemblyMatrixDisplacementReal {
	return &AssemblyMatrixDisplacementReal{
		conn, ctx, pb.NewAssemblyMatrixDisplacementRealClient(conn),
	}
}

func (a *AssemblyMatrixDisplacementReal) addElementaryMatrix(elementaryMatrix *pb.ElementaryMatrix) {
	a.client.AddElementaryMatrix(a.ctx, elementaryMatrix)
}

func (a *AssemblyMatrixDisplacementReal) setDOFNumbering(DOFNumbering) {
	a.client.SetDOFNumbering(a.ctx, &emptypb.Empty{})
}

func (a *AssemblyMatrixDisplacementReal) assemble() {
	a.client.Assemble(a.ctx, &emptypb.Empty{})
}

// MumpsSolver
type MumpsSolver struct {
	conn   *grpc.ClientConn
	ctx    context.Context
	client pb.MumpsSolverClient
}

func NewMumpsSolver(conn *grpc.ClientConn, ctx context.Context) *MumpsSolver {
	return &MumpsSolver{
		conn, ctx, pb.NewMumpsSolverClient(conn),
	}
}

func (s *MumpsSolver) factorize(AssemblyMatrixDisplacementReal) {
	s.client.Factorize(s.ctx, &emptypb.Empty{})
}

func (s *MumpsSolver) solve(field FieldOnNodes) FieldOnNodes {
	fieldOnNodesId, err := s.client.Solve(s.ctx, &pb.FieldOnNodesId{Id: field.fieldId})
	if err != nil {
		log.Fatalf("Failed to solve the system: %v", err)
	}
	return *NewFieldOnNodes(fieldOnNodesId.Id, s.conn, s.ctx)
}

// FieldOnNodes
type FieldOnNodes struct {
	conn    *grpc.ClientConn
	ctx     context.Context
	client  pb.FieldOnNodesClient
	fieldId int64
}

func NewFieldOnNodes(fieldId int64, conn *grpc.ClientConn, ctx context.Context) *FieldOnNodes {
	return &FieldOnNodes{
		conn, ctx, pb.NewFieldOnNodesClient(conn), fieldId,
	}
}

func (f *FieldOnNodes) printMedFile(path string) {
	fileInfo, err := os.Stat(path)
	if err == nil && fileInfo.IsDir() {
		log.Fatalf("Can't write into a directory: %s", path)
	}
	medFile, err := f.client.PrintMedFile(f.ctx, &pb.FieldOnNodesId{Id: f.fieldId})
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

func main() {
	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	aster := NewCodeAster("localhost:50051", ctx)
	defer aster.Close()
	// Mesh
	mesh := aster.Mesh()
	mesh.readMedFile("zzzz503a.mmed")
	// Model
	model := aster.Model(mesh)
	model.addModelingOnMesh(pb.Physics_Mechanics, pb.Modelings_Tridimensional)
	model.build()
	// Material
	YOUNG := 200000.0
	POISSON := 0.3
	acier := pb.Material{
		Elas: &pb.Elas{
			E:  YOUNG,
			Nu: POISSON,
		},
	}
	materialField := aster.MaterialField(mesh)
	materialField.addMaterialOnMesh(&acier)
	materialField.build()
	// Loads
	// - Displacement
	displacement := pb.DisplacementReal{
		Dx: 0.0, Dy: 0.0, Dz: 0.0, NameOfGroup: "Bas",
	}
	load1 := aster.ImposedDisplacementReal(model)
	load1.setValue(&displacement)
	load1.build()
	// - Pressure
	pressure := pb.PressureReal{
		Pres: 1000.0, NameOfGroup: "Haut",
	}
	load2 := aster.DistributedPressureReal(model)
	load2.setValue(&pressure)
	load2.build()
	// Physical Problem
	study := aster.PhysicalProblem(model, materialField)
	study.addLoad(&load1)
	study.addLoad(&load2)
	study.computeDOFNumbering()
	// Discrete Computation
	discreteComputation := aster.DiscreteComputation()
	forces := discreteComputation.getNeumannForces(1.0)
	elementaryStiffnessMatrix := discreteComputation.getLinearStiffnessMatrix(false)
	elementaryDualStiffnessMatrix := discreteComputation.getDualStiffnessMatrix(false)
	// DOFNumbering
	dofNumbering := aster.DOFNumbering()
	dofNumbering.computeNumbering([]*pb.ElementaryMatrix{elementaryStiffnessMatrix, elementaryDualStiffnessMatrix})
	// Assembly Matrix
	assemblyMatrix := aster.AssemblyMatrixDisplacementReal()
	assemblyMatrix.addElementaryMatrix(elementaryStiffnessMatrix)
	assemblyMatrix.addElementaryMatrix(elementaryDualStiffnessMatrix)
	assemblyMatrix.setDOFNumbering(dofNumbering)
	assemblyMatrix.assemble()
	// Mumps Solver
	solver := aster.MumpsSolver()
	solver.factorize(assemblyMatrix)
	result := solver.solve(forces)
	result.printMedFile("zzzz503a.rmed")
}

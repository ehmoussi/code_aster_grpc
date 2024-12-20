package main

import (
	aster_client "astergrpc/astergrpc_go"
	aster_pb "astergrpc/interfaces/go"
	"context"
	"sync"
	"time"
)

func main() {
	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	aster := aster_client.NewCodeAster("localhost:50051", ctx)
	defer aster.Close()
	// Stream the logs
	var wg sync.WaitGroup
	aster.StreamLog(&wg)
	// Mesh
	mesh := aster.Mesh()
	mesh.ReadMedFile("zzzz503a.mmed")
	// Model
	model := aster.Model(mesh)
	model.AddModelingOnMesh(aster_pb.Physics_Mechanics, aster_pb.Modelings_Tridimensional)
	model.Build()
	// Material
	YOUNG := 200000.0
	POISSON := 0.3
	acier := aster_pb.Material{
		Elas: &aster_pb.Elas{
			E:  YOUNG,
			Nu: POISSON,
		},
	}
	materialField := aster.MaterialField(mesh)
	materialField.AddMaterialOnMesh(&acier)
	materialField.Build()
	// Loads
	// - Displacement
	displacement := aster_pb.DisplacementReal{
		Dx: 0.0, Dy: 0.0, Dz: 0.0, NameOfGroup: "Bas",
	}
	load1 := aster.ImposedDisplacementReal(model)
	load1.SetValue(&displacement)
	load1.Build()
	// - Pressure
	pressure := aster_pb.PressureReal{
		Pres: 1000.0, NameOfGroup: "Haut",
	}
	load2 := aster.DistributedPressureReal(model)
	load2.SetValue(&pressure)
	load2.Build()
	// Physical Problem
	study := aster.PhysicalProblem(model, materialField)
	study.AddLoad(&load1)
	study.AddLoad(&load2)
	study.ComputeDOFNumbering()
	// Discrete Computation
	discreteComputation := aster.DiscreteComputation()
	forces := discreteComputation.GetNeumannForces(1.0)
	elementaryStiffnessMatrix := discreteComputation.GetLinearStiffnessMatrix(false)
	elementaryDualStiffnessMatrix := discreteComputation.GetDualStiffnessMatrix(false)
	// DOFNumbering
	dofNumbering := aster.DOFNumbering()
	dofNumbering.ComputeNumbering([]*aster_pb.ElementaryMatrix{elementaryStiffnessMatrix, elementaryDualStiffnessMatrix})
	// Assembly Matrix
	assemblyMatrix := aster.AssemblyMatrixDisplacementReal()
	assemblyMatrix.AddElementaryMatrix(elementaryStiffnessMatrix)
	assemblyMatrix.AddElementaryMatrix(elementaryDualStiffnessMatrix)
	assemblyMatrix.SetDOFNumbering(dofNumbering)
	assemblyMatrix.Assemble()
	// Mumps Solver
	solver := aster.MumpsSolver()
	solver.Factorize(assemblyMatrix)
	result := solver.Solve(forces)
	result.PrintMedFile("zzzz503a.rmed")
	wg.Wait()
}

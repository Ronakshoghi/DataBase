#include "Includes.h"
#include "ConsoleOutput.h"
#include "Settings.h"
#include "PhaseField.h"
#include "Initializations.h"
#include "BoundaryConditions.h"
#include "RunTimeControl.h"
#include "Orientations.h"
#include "Mechanics/ElasticProperties.h"
#include "Mechanics/ElasticitySolverSpectral.h"
#include "Mechanics/CrystalPlasticity.h"
#include "Tools/MicrostructureAnalysis.h"
#include "Crystallography.h"
#include <sys/time.h>


using namespace std;
using namespace openphase;

void WriteStressStrain(CrystalPlasticity& CP, PhaseField& Phase, ElasticProperties& EP, int tStep, double RealTime, string FileName, double& EqStrain, double& EqStress);
double get_wall_time();
int main(int argc, char *argv[])
{
#ifdef MPI_PARALLEL
    int provided = 0;
    int rank;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &MPI_RANK);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &MPI_SIZE);
    {
#endif

    string InputFile = argv[1];
	Settings                    OPSettings(InputFile);
	RunTimeControl              RTC(OPSettings, InputFile);
	BoundaryConditions          BC(OPSettings, InputFile);
	PhaseField                  Phi(OPSettings);
	ElasticProperties           EP(OPSettings, InputFile);
	ElasticitySolverSpectral    ES(OPSettings);
	CrystalPlasticity           PFCP(OPSettings, InputFile);
    Orientations				OR(OPSettings);
    Crystallography				CR(OPSettings, InputFile);

    string OutFile       = OPSettings.TextDir +"outfile.txt";
    cout << OutFile << endl;
    double EqStrain;
    double EqStress;
    if(RTC.Restart)
        {
            cout << "Restart data being read! " << endl;
            Phi.Read(BC, RTC.tStart);
            EP.Read(BC, RTC.tStart);
            PFCP.Read(BC, RTC.tStart);

            EP.SetGrainsProperties(Phi);

            cout << "Restart: solving mechanical problem! " << endl;
            EP.SetEffectiveElasticConstants(Phi);
            EP.SetEffectiveTransformationStretches(Phi);
            ES.Solve(EP,  BC, RTC.dt);
            RTC.SimulationTime = RTC.dt * RTC.tStart;
            cout << "Restart Done!" << endl;
        }
        else
        {


        	Initializations::MatchBox(Phi, BC, OPSettings, 1);
            OR.SetGrainOrientationsFromFile(Phi, "orientations_goss_10_1331.csv");
            ConsoleOutput::WriteStandard("Initial Microstructure", "Set");

            EP.SetGrainsProperties(Phi);
            EP.SetEffectiveElasticConstants(Phi);
            EP.SetEffectiveTransformationStretches(Phi); //for transformation e.g. martensite

            PFCP.SetInitialHardening(Phi, BC);
            PFCP.SetGrainsProperties(Phi, EP);
            ConsoleOutput::WriteStandard("Grains Properties", "Set");


            remove(OutFile.c_str());
        }

    	//---------------------------------------------------------------------------------------------------------------------------------------------
            cout << "Entering the Time Loop!!!" << endl;
        //---------------------------------------------------------------------------------------------------------------------------------------------
        vStress stressIncrement = EP.AppliedStress/RTC.nSteps; //Divide load in nSteps
        vStress stressSumm;
        double wall0 = get_wall_time();

        for(RTC.tStep = RTC.tStart; RTC.tStep <= RTC.nSteps; RTC.IncrementTimeStep())
        {
        	EP.AppliedStress = stressIncrement*RTC.tStep; //Apply load increment
            PFCP.Solve(Phi, BC, EP, ES, RTC.dt, true);


            if (RTC.WriteToScreen())
            {/***********************************************/
                double E_En = EP.AverageEnergyDensity();

                //  Output to screen
                ConsoleOutput::WriteStandard("Simulation Time",RTC.SimulationTime);

                std::string message = ConsoleOutput::GetStandard("Elastic energy density", to_string(E_En));

                ConsoleOutput::WriteTimeStep(RTC, message);

                Phi.PrintVolumeFractions();
            }

            if (RTC.WriteVTK()) //What does each method do?
            {
//                Phi.WriteVTK(RTC.tStep, OPSettings);
                // EP.WriteStressesVTK(RTC.tStep, OPSettings);
                EP.WriteCauchyStressesVTK(RTC.tStep, OPSettings);
//                EP.WritePlasticStrainsVTK(RTC.tStep,OPSettings);
//                EP.WriteTotalRotationsVTK(RTC.tStep, OPSettings);
//                Phi.WriteDistortedVTK(RTC.tStep, OPSettings, EP);
//                PFCP.WriteVTK(Phi, OPSettings, EP, RTC.tStep, true);
//                PFCP.WriteAverageVTK(Phi,OPSettings,EP, RTC.tStep,true);
            }

            // Write to result file OutFile in each timestep
            WriteStressStrain(PFCP, Phi, EP, RTC.tStep, RTC.SimulationTime, OutFile, EqStrain, EqStress);
            // if (RTC.WriteRawData())
            // {
            //     Phi.Write(RTC.tStep);
            //     PFCP.Write(RTC.tStep);
            //     EP.Write(RTC.tStep);
            // }
            stressSumm+=stressIncrement;
            if (RTC.tStep == RTC.nSteps)
            {
            	cout << "Applied Stress in Loadstep" << EP.AppliedStress.tensor().print() << endl;
            	cout << "Equivalent Total Strain: " << EqStrain  << endl;
            }
        }
    #ifdef MPI_PARALLEL
        }
        MPI_Finalize ();
    #endif

        double wall1 = get_wall_time();
        cout << "Wall Time = " << wall1 - wall0 << endl;
        return 0;
}

void WriteStressStrain(CrystalPlasticity& CP, PhaseField& Phase, ElasticProperties& EP, int tStep, double RealTime, string FileName, double& EqStrain, double& EqStress)
{
    vStress Stresses;
    vStrain Strains;
    vStrain Strains_Plastic;
    double Norm = 0.0;
    double MisesStress;
	vStrain UnitStrain, StrainDev;
	vStress UnitStress, StressDev;
	vector<double>v = {1,1,1,0,0,0};
	size_t it = 0;

    OMP_PARALLEL_STORAGE_LOOP_BEGIN(i,j,k,EP.Stresses,0,reduction (vStressSUM:Stresses) reduction (vStrainSUM:Strains) reduction (vStrainSUM:Strains_Plastic) reduction(+:Norm))
    for (auto it = Phase.Fields(i,j,k).cbegin(); it < Phase.Fields(i,j,k).cend(); ++it)
    {
        if(it->value > 0.0) // Why check PhaseField value?
        {
            int thPhaseIndex = Phase.FieldsProperties[it->index].Phase;
			if (CP.PhaseCrystalPlasticityMode[thPhaseIndex].Plasticity) // Does this check whether plastic deformation happened or just wether plasticity module is enabled for that cell?
			{
				#ifdef MPI_PARALLEL
					if(MPI_RANK == 0)
					{
				#endif
					//if(tStep == 1000)
					//{
					//	#pragma omp critical
					//	cout << Phase.FieldsStatistics[it->index].Orientation.getEulerAngles(false).print_degree() << " index: " << it->index << endl;
					//}
				#ifdef MPI_PARALLEL
					}
				#endif
				Stresses += EP.CauchyStress(i,j,k)* it->value;
				Strains += EP.StrainGreenLagrange(EP.DeformationGradientsTotal(i,j,k))* it->value;
				Strains_Plastic += EP.PlasticStrains(i, j, k)* it->value;
				//cout << Stresses.tensor().print() << endl;
				Norm += it->value; //Counting the number of elements
			}
        }
    }
    OMP_PARALLEL_STORAGE_LOOP_END

#ifdef MPI_PARALLEL
    double tmpStresses = Stresses;
    MPI_Allreduce(&tmpStresses, &Stresses, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    double tmpStresses11 = Stresses11;
    MPI_Allreduce(&tmpStresses11, &Stresses11, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    double tmpNorm = Norm;
    MPI_Allreduce(&tmpNorm, &Norm, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
#endif

    if(Norm > 0.0) //homogenization: My grains all have the same volume so this should be the volume average
    {
        Stresses /= Norm;
        Strains /= Norm;
        Strains_Plastic /= Norm;
    }

#ifdef MPI_PARALLEL
    if(MPI_RANK == 0)
    {
#endif

	UnitStrain.set_to_unity();
	UnitStress.unpack(v, it);

	StrainDev = Strains-UnitStrain*1./3*Strains.trace();
	EqStrain = sqrt(2./3.)*StrainDev.norm();

	StressDev = Stresses-UnitStress*1./3.*Stresses.trace();
	EqStress = sqrt(3./2.)*StressDev.norm();
	MisesStress = Stresses.Mises(); //consistent to my EqStress defintion
	//cout << sqrt(2./3.)*StrainDev.norm()<< endl;
	//cout << StrainDev.tensor().print() << endl;

    fstream output_file;
    if (tStep == 0)
    {
        output_file.open(FileName.c_str(), ios::out);
        output_file << left << "S11"
        			<< ';' <<left << "S22"
					<< ';' <<left <<  "S33"
					<< ';' <<left <<  "S12"
					<< ';' <<left <<  "S23"
					<< ';' <<left <<  "S13"
					<< ';' <<left <<  "E11"
					<< ';' <<left << "E22"
					<< ';' <<left <<  "E33"
					<< ';' <<left <<  "E12"
					<< ';' <<left <<  "E23"
					<< ';' <<left <<  "E13"
					<< ';' <<left <<  "EP11"
					<< ';' <<left << "EP22"
					<< ';' <<left <<  "EP33"
					<< ';' <<left <<  "EP12"
					<< ';' <<left <<  "EP23"
					<< ';' <<left <<  "EP13"
					<< ';' <<left <<  "Seq"
					<< ';' <<left <<  "Eeq"
        			<< ';' <<left <<  "SvM";
        output_file << endl;
        output_file.close();
    }


    output_file.open(FileName.c_str(), ios::app);
    output_file << left << Stresses.write(16, ';')
    			<< left << Strains.write(16, ';')
    			<< left << Strains_Plastic.write(16, ';')
				<< left << EqStress
				<< left << ';'
				<< left << EqStrain
				<< left << ';'
				<< left << MisesStress;
    output_file << endl;
    output_file.close();
#ifdef MPI_PARALLEL
    }
#endif


}

double get_wall_time(){
    struct timeval time;
    if (gettimeofday(&time,NULL)){
        //  Handle error
        return 0;
    }
    return (double)time.tv_sec + (double)time.tv_usec * .000001;
}
/*
void WriteGlobalStressesVTK(ElasticProperties& EP, PhaseField& Phi, const int tStep,
        const Settings& locSettings, const int precision) const
{
    std::vector<VTK::Field_t> ListOfFields;
    ListOfFields.push_back(VTK::Field_t {"Stresses", [EP](int i,int j,int k){return EP.Stresses(i, j, k);}});
    ListOfFields.push_back(VTK::Field_t {"von Mises", [EP](int i,int j,int k){return EP.Stresses(i, j, k).Mises();}});
    ListOfFields.push_back(VTK::Field_t {"Pressure", [EP](int i,int j,int k){return EP.Stresses(i, j, k).Pressure();}});

    std::string Filename = UserInterface::MakeFileName(VTKDir, "Stresses_", tStep, ".vts");
    VTK::Write(Filename, locSettings, ListOfFields, precision);
}
*/

#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <chrono>
#include<math.h>
#include <random>
#include "force_calculation.h"



using namespace std;


const int    iters       = 300000; //Number of Iterations
const double final_time  = 300;
const double sigma       = 1;
const double epsilon     = 1;
const int    n           = 8;
const int    N           = n*n; //Number of Particles
const double spacing     = 4; //1.1;
const double L           = n*spacing + 50;
const double cut_off     = 0.7*L/2;//0.95 * L/2;
const double delta       = 0.1;
const double dt          = final_time /iters;



//const int    iters       = 1000000; //Number of Iterations
//const double final_time  = 500;
//const double sigma       = 1;
//const double epsilon     = 1;
//const double spacing     = 1.3;//0.5*cut_off;
//const int    n           = 8; //floor(L/spacing);
//const int    N           = n*n; //Number of Particles
//const double L           = n*spacing;
//const double cut_off     = 0.9 * L/2;
//const double delta       = 0.1;
//const double dt          = final_time /iters;


struct Particle particles[N];
struct Force F[N];

double modulo(double n, double d){

    double mod = fmod(n,d);

    if (mod < 0){
       mod = d+mod;
    }
return mod;
}


int main(){

    if (spacing <= pow(2,1/6)*sigma ){
        cout << "Warning: Particles are initialized within the repulsive range" << endl;
    }

    if (spacing > cut_off){
        cout << "Warning: Particles are too widely spaced" << endl;
    }


    // construct a trivial random generator engine from a time-based seed:
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator (seed);
    std::normal_distribution<double> distribution (0.0,1.0);

    // Coefficients for smooth cut-off in the LJ potential.
    double *polynomial_coeffs;
    polynomial_coeffs = determine_polynomial_coeffs(sigma,epsilon,cut_off,delta);

    /////////////////////////Output Parameters////////////////////////
    ofstream out {"parameters.csv"};
    out<<fixed<<setprecision(4);
    out << "N" <<"," <<"iters" <<","<< "sigma" <<","<< "epsilon" <<","<<"cut_off" <<","<<"delta"<<","<< "a" <<","<< "b" <<","<< "c" << ","<< "d" <<
    "," <<"L" <<  endl;
    out << N << "," << iters <<"," <<sigma << "," << epsilon << "," << cut_off << "," <<delta << "," << polynomial_coeffs[0]  << "," <<
    polynomial_coeffs[1] << "," << polynomial_coeffs[2] << "," << polynomial_coeffs[3]  << "," << L << endl;

    out.close();

    // make it such that n**2 >N, can control the spacing through this parameter


    cout << "Beginning initialisation..."<<endl;
    int k =0;
    for (int i=0;i<n;i++){
        for (int j=0;j<n;j++){
            if (k<N){

                particles[k].x = (i + 0.5)*spacing;
                particles[k].y = (j + 0.5)*spacing;

                particles[k].vx = 0;//distribution(generator);
                particles[k].vy = 0;//distribution(generator);
                cout << particles[k].x << " " << particles[k].y << " " << particles[k].vx << " " << particles[k].vy << endl;
            }
            k++;

        }

    }
    cout<< "...1 done." << endl;

    force_calculation(F,particles,polynomial_coeffs);

    cout<< "...2 done." << endl;

    ////Open an output file and read out initial conditions/////
    ofstream mout {"molecular_data.csv"};
    mout<< "x,y,vx,vy,K,W"<<endl;
    for(int i = 0; i<N; i++){
        mout << particles[i].x << "," << particles[i].y<<","<<particles[i].vx<<","<<particles[i].vy<<","<<particles[i].K<<","<<particles[i].W<<endl;
    }

    for (int t=0; t<iters-1; t++) {

        for (int i=0; i<N; i++) {
            particles[i].vx += 0.5*dt*F[i].x;
            particles[i].vy += 0.5*dt*F[i].y;

            particles[i].x += dt*particles[i].vx;  // modulo L to implement periodicity
            particles[i].x = modulo(particles[i].x, L);  // modulo L to implement periodicity

            particles[i].y += dt*particles[i].vy;
            particles[i].y = modulo(particles[i].y, L);
        }

        force_calculation(F,particles,polynomial_coeffs);

        for (int i=0; i<N; i++) {
            particles[i].vx += 0.5*dt*F[i].x;
            particles[i].vy += 0.5*dt*F[i].y;

            particles[i].K = 0.5*(particles[i].vx * particles[i].vx + particles[i].vy * particles[i].vy);
        }

        cout<< "Timestep "<< t+1 << " of " << iters-1 << " done."<<endl;

        for(int i = 0; i<N; i++){
            mout << particles[i].x << "," << particles[i].y<<","<<particles[i].vx<<","<<particles[i].vy<<","<<particles[i].K<<","<<particles[i].W<<endl;
        }
    }
    mout.close();
    return 0;
}

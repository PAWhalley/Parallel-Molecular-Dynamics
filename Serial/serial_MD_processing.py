import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def separations_histogram(time_step,separations):
    hist,bins = np.histogram(separations[time_step,:])
    return hist, bins

def LJ_potential(epsilon,sigma,rc,delta,r,a,b,c,d):
    if(r<rc):
        potential = 4*epsilon*(np.power(sigma/r,12)-np.power(sigma/r,6))
    elif(r<rc+sigma):
        potential = a + b*r + c*r**2+ d*r**3
    else: 
        potential = 0
        
    return potential

## Importing data
imported_data = pd.read_csv("molecular_data.csv",sep = ' ')
parameters = pd.read_csv("parameters.csv", sep = ' ')

N = parameters.N.to_numpy()[0]
sigma = parameters.sigma.to_numpy()[0]
epsilon = parameters.epsilon.to_numpy()[0]
rc = parameters.cut_off.to_numpy()[0]*sigma
delta = parameters.delta.to_numpy()[0]
nsteps = parameters.iters.to_numpy()[0]
a = parameters.a.to_numpy()[0]
b = parameters.b.to_numpy()[0]
c = parameters.c.to_numpy()[0]
d = parameters.d.to_numpy()[0]


x = imported_data.x.to_numpy()
y = imported_data.y.to_numpy()
vx = imported_data.vx.to_numpy()
vy = imported_data.vy.to_numpy()

#

## Reshaping to get a matrix where each column is a particle and each row a time step.
x = np.reshape(x,(nsteps,N))
y = np.reshape(y,(nsteps,N))
vx = np.reshape(vx,(nsteps,N))
vy = np.reshape(vy,(nsteps,N))

## Calculating the separations, kinetic energy, and potential energy of all particles at each time step.
separations = np.zeros((nsteps, int(N*(N-1)/2)))
kinetic_energy = np.zeros((nsteps,N))
potential_energy = np.zeros((nsteps,N))

total_kinetic_energy = np.zeros(nsteps)
total_potential_energy = np.zeros(nsteps)
total_energy = np.zeros(nsteps)

for step in range(nsteps):
    kinetic_energy[step,:] = 0.5 * (np.power(vx[step,:],2)+np.power(vy[step,:],2))
    for i in range(N):
        for j in range(i+1,N):
            separations[step,i] = np.power(np.power(x[step,i]-x[step,j],2)+np.power(y[step,i]-y[step,j],2),1/2)
            potential_energy[step,i] = potential_energy[step,j] = potential_energy[step,i] + 0.5*LJ_potential(epsilon,sigma,rc,delta,separations[step,i],a,b,c,d)
            
    total_kinetic_energy[step] = np.sum(kinetic_energy[step:])
    total_potential_energy[step] = np.sum(potential_energy[step:])
    total_energy[step] = total_kinetic_energy[step] + total_potential_energy[step]
            

            
    
# Total energy of the system          
fig,ax = plt.subplots(1,1)

ax.plot(total_energy)
ax.set_xlabel('Time step')
ax.set_ylabel('Total Energy')
ax.set_title('Total energy')

# Snapshot of particles at a given timestep            
fig,ax = plt.subplots(1,1)

ax.scatter(x[nsteps-1,:],y[nsteps-1,:], marker = 'x')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Particle positions at timestep=' + str(nsteps-1))

# Histogram of particle separations            
fig,ax = plt.subplots(1,1)

ax.hist(separations[nsteps-1,:], bins = 'auto')
ax.set_xlabel('Separation')
ax.set_ylabel('Frequency')
ax.set_title('Separation histogram')

if(N==2):
## Plots for a single pair of particles.
    fig,ax = plt.subplots(1,1)
    
    ax.plot(y[:,0], label = 'Particle 1')
    ax.plot(y[:,1], label = 'Particle 2')
    ax.set_xlabel('Time step')
    ax.set_ylabel('y')
    ax.set_title('y positions')
    ax.legend()
    
    fig,ax = plt.subplots(1,1)
    
    ax.plot(x[:,0], label = 'Particle 1')
    ax.plot(x[:,1], label = 'Particle 2')
    ax.set_xlabel('Time step')
    ax.set_ylabel('x')
    ax.set_title('x positions')
    ax.legend()



















































#sigma = 1
#epsilon = 1
#
#rc = 3*sigma
#delta = 0.1
#
#r = np.linspace(0.1,10*sigma,1000)
#
#A = np.array([[1,rc,rc**2,rc**3],[0,1,2*rc,3*rc**2],[1,rc+delta,np.power(rc+delta,2),np.power(rc+delta,3)],[0,1,2*(rc+delta),3*np.power(rc+delta,2)]])
#b = np.array([4*epsilon*(np.power(sigma/rc,12)-np.power(sigma/rc,6)),24*epsilon*((np.power(sigma,6)/np.power(rc,7))-(2*np.power(sigma,12)/np.power(rc,13))) , 0, 0])
#
#a,b,c,d = np.linalg.solve(A,b)
#
#LJ = 4*epsilon*(np.power(sigma/r,12)-np.power(sigma/r,6))
#polynomial =  a + b*r + c*r**2+ d*r**3
#
#fig,ax = plt.subplots(1,1)
#ax.plot(r,LJ, label = 'Lennard-Jones Potential')
#ax.plot(r,polynomial, label = 'Polynomial cut-off')
#ax.set_xlabel('r')
#ax.set_ylabel('potential')
#ax.axvline(x=rc,color = 'b')
#ax.axvline(x=rc+delta, color = 'r')
#ax.axhline(y=0, color ='k')
#ax.set_ylim(-1,1)
#ax.legend()
#ax.set_title('Illustration of smooth cut-off for the L-J potential')
#
#
#rc = 3.05#np.sqrt(8);
#
#pot_deriv1 =  24*epsilon*((np.power(sigma,6)/np.power(rc,7))-(2*np.power(sigma,12)/np.power(rc,13)))
#pot_deriv2 = b+2*c*rc+3*d*np.power(rc,2)
#
#fx = (pot_deriv2/rc)*(-3.05)
#fy = (pot_deriv2/rc)*(0)

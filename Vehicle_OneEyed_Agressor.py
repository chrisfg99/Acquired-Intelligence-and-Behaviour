import numpy as np
import matplotlib.pyplot as plt

def run(T,initial_pos,initial_bearing,geno,plot_flag):

    #runs a simple agent described by a geno and returns the trajectory
    #the light is at [0 0]

    #input
    #T is the time you want run it for
    #pos initial position
    #bearing initial bearing (degrees) e.g [90; 90]
    #geno genotype e.g [w_ll w_lr w_rl w_rr bl br]
    #plot_flag set to tru to output the figure

    #output a 2-d vector with the x and y coordinates
    
    #run a simple agent
    #geno = np.array([-1, 0, 0, -.4, 1, 0.5])
    #initial_pos = [1,1]
    #T=100
    #out  = simple_agent.run(T,initial_pos,90,geno,1)
    

    # Initial setup
    dt=0.05
    R =0.05 #radius
    b = 45 #(degrees) sensor anglr

    #convert geno parameters
    w_l = geno[0] #left motor to sensor
    w_r = geno[1] #right motor to sensor
    bl = geno[2]
    br = geno[3]
    s_pos = np.zeros((2,1))
    
    sensor_gain = 1
    motor_gain =1
    vl=0;vr=0
    #convert to radians
                                                
    initial_bearing = initial_bearing/360*2*np.pi
    b=b/360*2*np.pi
    
    pos = np.zeros((2,int(T/dt)))
    bearing = np.zeros((1,int(T/dt)))
    pos[:,0] = initial_pos
    bearing[:,0] = initial_bearing
    
   
    for i in range(1, int(T/dt)):
        vc = (vl+vr)/2
        va = (vr-vl)/(2*R)
        pos[0,i] = pos[0,i-1]+ dt*vc*np.cos(bearing[0,i-1])
        pos[1,i] = pos[1,i-1]+ dt*vc*np.sin(bearing[0,i-1])
        bearing[0,i] = np.mod(bearing[0,i-1] + dt*va,2*np.pi)
        
        # Calculate sensor position
        s_pos[0] = pos[0,i] + R*np.cos(bearing[0,i]+b)
        s_pos[1] = pos[1,i] + R*np.sin(bearing[0,i]+b)

        # Calculate (square) distance to element
        dl = np.sqrt((s_pos[0])**2+(s_pos[1])**2)   

        #  Calculate local intensity
        i = sensor_gain/dl

        #Calculate Motor intensities from sensor
        lm = i*w_l + bl
        rm = i*w_r + br

        #  Scale by motor gains
        vl =motor_gain*lm
        vr =motor_gain*rm
     
    if plot_flag==1:
        plt.plot(pos[0,:],pos[1,:])
       
        #final postion
        x=pos[0,int(T/dt)-1]
        y= pos[1,int(T/dt)-1]
        f_bearing = bearing[0,int(T/dt)-1]

        # Calculate left sensor position
        s_pos[0] = x + R*np.cos(f_bearing+b)
        s_pos[1] = y + R*np.sin(f_bearing+b)

        plt.plot(0,0,marker='.',markersize=30,color='yellow') 
        plt.plot(0,0,marker='o',markersize=10,color='black') 
       
    # Plot  sensors
       #
        plt.plot(s_pos[0],s_pos[1],marker='.',markersize=10,color='red') 

    
        # Plot body
        plt.plot( x, y,marker='.',markersize=10,color='blue') 
        plt.plot(x,y,marker='o',markersize=10,color='black') 
        #Plot trajectory
        plt.show()
        
    
    return pos

geno = np.array([2,1,-1,0])
initial_pos = [-1,-1]
T=12
run(T,initial_pos,270,geno,1)


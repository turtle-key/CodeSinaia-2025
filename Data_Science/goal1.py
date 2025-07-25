import math

def calculate_p(p_x, p_y, p_z):    #This function calculates the momentum of a particle given its components.
    return math.sqrt(p_x ** 2 + p_y ** 2 + p_z ** 2)     #uses the formula for p

def calculate_pT (p_x, p_y):    #This function calculates the transverse momentum of a particle given its x and y components.    
    return math.sqrt(p_x **2 + p_y ** 2)
def calculate_pseudorapidity(p, p_z):               #pseudorapidity is the n with a long end
    return math.log((abs(p) + p_z) / (abs(p) - p_z)) / 2 

def calculate_azimuthal_angle(p_x, p_y):
    phi = math.atan2(p_x, p_y)
    return phi

def check_type (pdg_code):      #this function checks the type of particle based on the pdg code
    pass


#TODO: Open the input file, read the first line to get event_id and num_particles,
#       then read the rest of the lines into lines_list as lists of strings.
#pdg code 211, -211
with open("/Users/mihai-edi/Projects/Code Sinaia/Data_Science/Dataset/output-Set0.txt", "r") as infile:
    index = 0
    for line in infile:
        parts = line.strip().split()
        if index == 0:
            event_id = int(parts[0])
            num_particles=int(parts[1])
            print(f"event id is {event_id} and there are {num_particles} particles\n")  
        else:
            print(f"For particle {index}")
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2])
            particle= int(parts[3])    
            if(abs(particle) == 211 or particle == 111):
                output = "This is a "
                pion = "positive" if particle > 0 else "negative" 
                pion = "neutral" if particle == 111 else pion
                print(output + pion + " pion")
                print(f"pseuorapidity= {calculate_pseudorapidity(calculate_p(x, y, z), z)}")
                print(f"pT = {calculate_pT(x, y)}")
                print(f"azimuthal angle is {calculate_azimuthal_angle(x, y)}\n")
            else:
                print("This is not a pion\n")
        index+=1 
print("event id is", event_id, "and there are", num_particles, "particles")       #print to show the events id and no of particles in the event


# TODO: Loop through each particle in lines_list, convert values to float,
#       call the analysis/calculation functions, and print the results as shown.
    

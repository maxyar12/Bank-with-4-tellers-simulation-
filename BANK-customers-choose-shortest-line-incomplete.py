# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:40:26 2019

@author: maxya
"""
# -*- coding: utf-8 -*-
''' time-advance- bank with 4 teller, two types of accounts '''

import numpy as np       # DEPENDENCY - to make random numbers easily

def simulate(numXacts,wantreport):
    
 #--INITIALIZE STATISTICS (stats accumulated for departed customers up to CLOCK)
    Bs = [0,0,0,0]          # total server (teller) busy times
    Sbiz = 0                # total response time for business customers
    Sgeneral = 0            # total response time for general customers
    S = 0                   # total response time for all customers (combined)
    Nd = 0                  # total number of departures 
    numGeneral = 0          # total number of general account departures
    numBiz = 0              # total number of biz account departures
    delayTime = 0           # total delay time
    numDelayed = 0          # total number of customers who had to wait in line
    delayedGTone = 0        # total number of customers who waited > 1 min in line
    avgBizLineLength = 0    # average line length for business lines
    avgGenLineLength = 0    # average line length for general lines
    avgLineLength = 0       # average line length for all lines (combined)
    
    # INITIZIALIZE SYSTEM VARS and LISTS -------------------------------------
    
    # event_types identifier and description:
    # 0 = arrival event 
    # 1 = Departure event teller 1 - general account
    # 2 = Dearture event  teller 2 - general account
    # 3 = departure event teller 3 - biz account
    # 4 = Departure event  teller 4 - biz account
    
    CLOCK = 0                # simulation time
    LQs = [0,0,0,0]          # num of cust in queue for each teller
    LSs = [0,0,0,0]          # state of each teller (0-idle or 1-busy)
    lines = [[],[],[],[]]    # list of cust in line or being served for each teller
    FEL = []                 # future event notice list
    C_ID = 1                 # counter to keep track of customers
    
#---- CUSTOMER NUMBER ONE ENTERS THE BANK -INITIALIZATION-------------------------
      
    if np.random.random() < 0.34:                 # business account
        if np.random.random() <= 0.5:                        # customer chooses teller 3
            lines[2].append(customer(C_ID,CLOCK))            # add cust to line 3
            FEL.append(eventnotice(3,biztime(),C_ID))       # add dep notice to FEL
            LSs[2] = 1                                       # set teller 3 busy
        else:                                               # cust chooses teller 4 
            lines[3].append(customer(C_ID,CLOCK))           # add cust to line 4
            FEL.append(eventnotice(4,biztime(),C_ID))       # add dep notice to FEL
            LSs[3] = 1                                      # set teller 4 busy
    else:                                           # general account
        if np.random.random() <= 0.5:                        # customer chooses teller 1
            lines[0].append(customer(C_ID,CLOCK))            # add customer to line 1
            FEL.append(eventnotice(1,gentime(),C_ID))       # add dep notice to FEL
            LSs[0] = 1                                       # set teller 1 busy
        else:                                               # customer chooses teller 2
            lines[1].append(customer(C_ID,CLOCK))            # add customer to line 2
            FEL.append(eventnotice(2,gentime(),C_ID))       # add dep notice to FEL
            LSs[1] = 1                                       # set teller 2 busy
    C_ID += 1    
    FEL.append(eventnotice(0,iatime(),C_ID))          # add next arrival notice to FEL
    
    # -------MAIN PROGRAM ------------
    
    while Nd < numXacts:    
              
        FEL = sorted(FEL, key=lambda x: x.futuretime)   # SORT THE FEL BY TIME
        IE = FEL.pop(0)                                 # remove IMMINENT EVENT
        advance = IE.futuretime - CLOCK                 # get CHANGE IN TIME
        CLOCK = IE.futuretime                           # advance the clock
        et = IE.eventtype
        
        if LSs[0] == 1:
            Bs[0] = Bs[0] + advance
        if LSs[1] == 1:
            Bs[1]= Bs[1] + advance
        if LSs[2] == 1:
            Bs[2] = Bs[2] + advance    
        if LSs[3] == 1:
            Bs[3] = Bs[3] + advance
        
        avgBizLineLength = avgBizLineLength + 0.5*advance*(LQs[2]+LQs[3])
        avgGenLineLength = avgGenLineLength + 0.5*advance*(LQs[0]+LQs[1])
        
        if et == 0:                            #arrival logic         
            if np.random.random() < 0.34:                #biz account
                if LQs[2] < LQs[3]:
                    if LSs[2] == 1:
                        LQs[2] = LQs[2] + 1
                        lines[2].append(customer(IE.customerid,CLOCK))
                    else:
                        LSs[2] = 1
                        lines[2].append(customer(IE.customerid,CLOCK))
                        FEL.append(eventnotice(3,CLOCK+biztime(),IE.customerid))
                elif LQs[2] == LQs[3]:
             # ----------------------------------------------------------------------                                  
             # STUDENT - YOU MUST FILL IN EVERYTHING ELSE THAT GOES HERE
             # SOME CODE IS MISSING - ITS YOUR JOB TO FILL IT IN BELOW

             
             
             #---------------------------------------------------------------------------------                
            C_ID += 1        
            FEL.append(eventnotice(0,CLOCK + iatime(),C_ID))
        
        else:                                                 #departure logics
            departing = next((x for x in lines[et-1] if \
                              x.customerid == IE.customerid), None) 
            S = S + CLOCK - departing.arrivaltime
            if (et == 1 or et == 2):
                Sgeneral = Sgeneral + CLOCK - departing.arrivaltime
                numGeneral = numGeneral + 1
            else:
                Sbiz = Sbiz + CLOCK - departing.arrivaltime
                numBiz = numBiz + 1
            Nd = Nd + 1
            lines[et-1].remove(departing)
            
            if LQs[et-1] > 0:
                LQs[et-1] = LQs[et-1] - 1
                lines[et-1] = sorted(lines[et-1], key=lambda x: x.arrivaltime)  
                firstinline = lines[et-1][0]
                delayTime = delayTime + CLOCK - firstinline.arrivaltime
                numDelayed = numDelayed + 1
                if (CLOCK - firstinline.arrivaltime) >= 1:
                    delayedGTone = delayedGTone + 1
                if (et == 1 or et == 2):   
                    FEL.append(eventnotice(et,CLOCK + gentime(),firstinline.customerid))
                else:
                    FEL.append(eventnotice(et,CLOCK + biztime(),firstinline.customerid))
            else:
                LSs[et-1] = 0

    #-------REPORT GENERATOR-----------------------
    
    if wantreport == 1:
        print("simulation run length = ","%.3f" %  CLOCK) 
        print("number of departures= ", Nd) 
        print("U_1 = ", "%.3f" %  (Bs[0]/CLOCK))
        print("U_2 = ", "%.3f" %  (Bs[1]/CLOCK))
        print("U_3 = ", "%.3f" %  (Bs[2]/CLOCK))
        print("U_4 = ", "%.3f" %  (Bs[3]/CLOCK))
        print("S_biz = ", "%.3f" %  (Sbiz/numBiz))
        print("S_general = ", "%.3f" %  (Sgeneral/numGeneral))
        print("S_all_customers = ", "%.3f" %  (S/Nd)) 
        print("average delay time (over all customers)", "%.3f" %  (delayTime/Nd))
        print("%delayed > 1 minute (of those who were delayed at all)  = ","%.3f" %  (delayedGTone/numDelayed)) 
        print("%delayed > 1 minute over all customers = ","%.3f" %  (delayedGTone/Nd))
        print("average line length for biz customers = ","%.3f" %  (avgBizLineLength/CLOCK))   
        print("average line length for general customers = ","%.3f" %  (avgGenLineLength/CLOCK))
        print("average line length for all types of lines = ","%.3f" %  \
                       ((avgBizLineLength/CLOCK + avgGenLineLength/CLOCK)/2.0)   )
 
#------------ return statements -------------------   
    return " "
#----------------END SIMULATION------------------------
    
#---------classes and RN generation ------------------------
    
class customer():
    def __init__(self, customerid, arrivaltime):
        self.customerid = customerid
        self.arrivaltime = arrivaltime
        
class eventnotice():
    def __init__(self, eventtype, futuretime,customerid):
        self.eventtype = eventtype
        self.futuretime = futuretime
        self.customerid = customerid
        
def iatime():
    muA = 3
    return muA + np.random.uniform(-1,1)

def biztime():
    muS= 15
    return muS + np.random.uniform(-10,10)

def gentime():
    muSG = 6
    return muSG + np.random.uniform(-5,5)

if __name__ == '__main__':
    simulate(500000,1)

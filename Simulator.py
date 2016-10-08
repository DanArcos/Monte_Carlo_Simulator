from pandas import DataFrame;
from pandas import ExcelWriter;
import numpy as np;
import matplotlib.pyplot as plt;
from matplotlib.patches import Rectangle

#Function to generate normal random variables.
def run_simulation(trials, years, mean, risk):
    #Generate Random Normals
    data = np.random.normal(mean,risk,trials*years)
    data = data.reshape([trials,years])
    return (data)

#Function to grow hypothetical value
def grow_value(starting_value, normal_rvs,spending):
    normal_rvs = normal_rvs+1    
    for x in range(years):
        if x == 0:
            normal_rvs[:,x] = (normal_rvs[:,x]*starting_value)+spending[x]
            #print(sims[:,x])
        else:
            normal_rvs[:,x] = (normal_rvs[:,x-1]*normal_rvs[:,x])+spending[x]
            #print(sims[:,x])
    return normal_rvs

#Get median values for output
def get_percentiles(model):
    #Build columns    
    columns = []
    for i in range(years):
        columns.append(i+1)        
    df = DataFrame(columns = columns)
    for x in range(5,100,5):
         df.loc[x] = [np.percentile(model.T[n],x) for n in range(years)]    
    df[0] = starting_value
    
    #Reorder Columns!    
    cols = list(df)
    cols.insert(0, cols.pop(cols.index(0)))
    df = df.ix[:, cols]
    
    return (df)

def get_inflation_adjusted_percentiles(nominal_values, inflation_rate):
    real_values = nominal_values.copy()
    for column in real_values:
        real_values[column] = real_values[column]/((1+inflation_rate)**(column))
    return real_values        
    
def visualize_data(nominal_values, real_values):
    plt.figure(1, figsize = (10,7))
        
    #Plot Nominal Values
    plt.subplot(221)    
    ax1 = plt.gca()    
    #Plot Rectangles
    for x in range(5,years+1,5):
        ax1.add_patch(Rectangle((x - .5, nominal_values[x][5]), 1, nominal_values[x][95]-nominal_values[x][5], facecolor="skyblue"))
        ax1.add_patch(Rectangle((x - .5, nominal_values[x][25]), 1, nominal_values[x][75]-nominal_values[x][25], facecolor="orange"))
        ax1.add_patch(Rectangle((x - .5, nominal_values[x][40]), 1, nominal_values[x][60]-nominal_values[x][40], facecolor="grey"))
    
    plt.plot(nominal_values.iloc[0]) #Plot 5 percent line
    plt.plot(nominal_values.iloc[9])  #Plot 50 percent line
    plt.plot(nominal_values.iloc[18]) #Plot 95 percent line
    plt.xlabel("Year")
    plt.ylabel("Value ($)")
    plt.title("Portfolio Projection \n(Nominal)", fontweight = "bold")
    plt.grid(True)
    plt.legend(loc= 0)        
    
    #Plot Real Values    
    plt.subplot(222)
    ax2 = plt.gca()
    #Plot Rectangles    
    for x in range(5,years+1,5):
        ax2.add_patch(Rectangle((x - .5, real_values[x][5]), 1, real_values[x][95]-real_values[x][5], facecolor="skyblue"))
        ax2.add_patch(Rectangle((x - .5, real_values[x][25]), 1, real_values[x][75]-real_values[x][25], facecolor="orange"))
        ax2.add_patch(Rectangle((x - .5, real_values[x][40]), 1, real_values[x][60]-real_values[x][40], facecolor="grey"))
    
    plt.plot(real_values.iloc[0]) #Plot 5 percent line
    plt.plot(real_values.iloc[9])  #Plot 50 percent line
    plt.plot(real_values.iloc[18]) #Plot 95 percent line
    plt.xlabel("Year")
    plt.ylabel("Value ($)")
    plt.title("Portfolio Projection \n(Real)", fontweight = "bold")
    plt.grid(True)
    plt.legend(loc= 0)
    plt.show()

def export_to_excel(nominal_values, real_values):
    writer = ExcelWriter("Output.xls", engine = 'xlsxwriter')
    nominal_values.to_excel(writer, sheet_name = "Nominal_Values")
    real_values.to_excel(writer, sheet_name = "Real_Values")
    writer.save()
    

def process_run(trials, years, starting_value, mean, risk, inflation_rate, spending):
    normal_rv = run_simulation(trials, years, mean, risk)
    growth_of_value = grow_value(starting_value, normal_rv, spending)
    nominal_values = get_percentiles(growth_of_value)
    real_values = get_inflation_adjusted_percentiles(nominal_values, inflation_rate)
    visualize_data(nominal_values, real_values)    
    export_to_excel(nominal_values, real_values)
        
trials = 40000
years = 20
mean = .0754
risk = .113
starting_value = 100
inflation_rate = .0225
spending = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

process_run(trials, years, starting_value, mean, risk, inflation_rate, spending)
 

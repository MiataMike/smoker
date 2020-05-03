import numpy as np

def steinhartHartCoe(T1,T2,T3,R1,R2,R3):
    # Temperatures in K
    # Resistors in ohm
    
    # Refs: https://www.azom.com/article.aspx?ArticleID=16601
    
    L1 = np.log(R1)
    L2 = np.log(R2)
    L3 = np.log(R3)
    Y1 = 1/T1
    Y2 = 1/T2
    Y3 = 1/T3
    gamma2 = (Y2 - Y1) / (L2 - L1)
    gamma3 = (Y3 - Y1) / (L3 - L1)
    C = (gamma3 - gamma2) / (L3 - L2) / (L1 + L2 + L3)
    B = gamma2 - C * (L1 * L1 + L1 * L2 + L2 * L2)
    A = Y1 - (B + L1 * L1 * C) * L1
    
    return [A, B, C]
    
    
    
def steinhartHartTemp(A, B, C, R):
    # Returns the temperature in K with resistance
    if R == 0.0:
        T1 = 9999.0
    else:
        T1 = 1 / (A + B * np.log(R) + C * np.log(R)**3)
        
    return T1

def F2K(T):
    # Convert fahrenheit to kelvin
    return (T - 32.0) * 5.0 / 9.0 + 273.15
    
def K2F(T):
    # Convert kelvin to fahrenheit
    return (T - 273.15) * 9.0 / 5.0 + 32

def voltDivR1(V0, V, R2):
    # Calculate R1 from voltage dividing circuit
    if V == 0.0:
        return 0.0
    else:
        return (V0 / V * R2) - R2

def populateHTML(data_dict):
    '''Open template file and save to index.html'''
    template_filename = '../TEMPLATE_index.html'
    output_filename = '../index.html'
    
    temp_file = open(template_filename,'r')
    temp_contents = temp_file.read()
    temp_file.close()
    
    
    for keys in data_dict:
        temp_contents = temp_contents.replace(keys,str(data_dict[keys]))
        
    out_file = open(output_filename, 'w+')
    out_file.write(temp_contents)
    out_file.close()




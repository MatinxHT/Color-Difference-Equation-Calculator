import numpy as np
import csv
import pandas as pd
import datetime
from deltaeformula import e_2000
from deltaeformula import e_cmc

print('--------------------openning--------------------\n','...')
#setting files name 
time = datetime.datetime.now()
LAB_Source_file = 'data.csv'

#starting read

print('--------------------starting to read data--------------------\n','...')
LAB_source_data = []
with open(LAB_Source_file) as csvfile:
    csv_reader = csv.reader(csvfile)
    LAB_data_header = next(csv_reader)
    for row in csv_reader:
        LAB_source_data.append(row)
LAB_source_data = [[float(x) for x in row] for row in LAB_source_data]
LAB_source_data = np.array(LAB_source_data)
LAB_data_header = np.array(LAB_data_header)

#reader debug
#couting data sum number
data_tuple = LAB_source_data.shape
total_sample_list = data_tuple[1]
total_sample_number =  data_tuple[0]

if total_sample_list != 6 :print('Worng data source!')
#print(total_sample_list)

print('successful read ',total_sample_number,' sample data')
#print(LAB_source_data) #show the data which csv.reader read
#print(LAB_data_header.shape) #show the shape of header
#print(LAB_source_data[0][2]) #[行][列]

#source data array debug area
#print(LAB_source_data.shape) #show data array shape
#print(LAB_source_data.ndim) #show data array ndim
#print(LAB_source_data.dtype,' all check finished') #show data array type
print('--------------------read finsished--------------------\n','...')

#data transform area
#formating var array
LAB_standard = np.empty([total_sample_number,3],dtype = float)
LAB_sample = np.empty([total_sample_number,3],dtype = float)
lab=np.array((1,1,1,1,1,1),dtype=float)
#LAB_sample = np.array([[],[]])

#check area

#print(LAB_standard.shape)
#print(LAB_standard.dtype)

#print(lab.shape)
#print(lab.dtype)
#print(lab.ndim)


#inputting data 
#print(LAB_source_data[i][0]) #check data

i = 0
while(i < total_sample_number):
    LAB_standard[i][0] = LAB_source_data[i][0] #inputing L*
    LAB_standard[i][1] = LAB_source_data[i][1] #inputing A*
    LAB_standard[i][2] = LAB_source_data[i][2] #inputing B*
    LAB_sample[i][0] = LAB_source_data[i][3] #inputing L
    LAB_sample[i][1] = LAB_source_data[i][4] #inputing A
    LAB_sample[i][2] = LAB_source_data[i][5] #inputing B
    i = i + 1
    
#checking standard and smples
#print(LAB_standard)
#print(LAB_standard.shape)
#print(LAB_sample)
#print(LAB_sample.shape)

#computing delta E 
print('--------------------starting to computing deltaE--------------------\n','...')
delta_e = np.empty([total_sample_number,1],dtype=float)
delta_ecmc = np.empty([total_sample_number,1],dtype=float)

i = 0
while(i < total_sample_number):
    e = e_2000(LAB_standard[i],LAB_sample[i],1,1,1)
    ecmc = e_cmc(LAB_standard[i],LAB_sample[i],2,1)
    delta_e[i] = e[0]
    delta_ecmc[i] = ecmc[0]
    i += 1

print('successful compute ',total_sample_number,' samples deltaE')
#print(delta_e)
#print(delta_e.shape)
print('--------------------success--------------------\n','...')

#result csv creating
print('--------------------starting creating Result-------------------\n','...')
#formating var list
Ls = list(range(total_sample_number))
As = list(range(total_sample_number))
Bs = list(range(total_sample_number))
L = list(range(total_sample_number))
A = list(range(total_sample_number))
B = list(range(total_sample_number))
elist = list(range(total_sample_number))
elist2 = list(range(total_sample_number))

#fuck martix up
delta_e = delta_e.flatten('A')
delta_ecmc = delta_ecmc.flatten('A')

#dropping num
i = 0
while(i < total_sample_number):
    Ls[i] = LAB_standard[i][0]
    As[i] = LAB_standard[i][1]
    Bs[i] = LAB_standard[i][2]
    L[i] = LAB_sample[i][0]
    A[i] = LAB_sample[i][1]
    B[i] = LAB_sample[i][2]
    elist[i] = delta_e[i]
    elist2[i] = delta_ecmc[i]
    i += 1 

#writting csv
resdict = {'L(std)': Ls, 'A(std)': As, 'B(std)': Bs,'L': L, 'a': A, 'b': B,'dEcmc(2:1)':elist2,'dE00':elist}
df = pd.DataFrame(resdict)

# saving
print('success')
df.to_csv('result.csv')

#ending
print('--------------------done--------------------')
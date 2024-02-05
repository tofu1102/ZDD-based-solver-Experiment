import matplotlib.pyplot as mplot
import numpy as np
import math

targetData=np.loadtxt('card-size-time-Z_sol-V.csv',delimiter=',')
#print(targetData.shape)
x=[]
y=[]
z=[]

for xyz in targetData:
    x.append(xyz[4])
    y.append(xyz[1])
    z.append(xyz[2])

# print(x)
# print(y)
# print(z)
fig=mplot.figure()
ax=fig.add_subplot(projection='3d')
ax.scatter(x,y,z)
ax.set_xlabel("X")
ax.set_ylabel("Y")
mplot.show()
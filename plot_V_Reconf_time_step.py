import matplotlib.pyplot as mplot
import numpy as np
import math

targetData=np.loadtxt('V-Reconf_time-step.csv',delimiter=',')
#print(targetData.shape)
#X:頂点数
#Y:Reconf_time
#Z:step
x=[]
y=[]
z=[]

for xyz in targetData:
    x.append(xyz[0])
    y.append(math.log10(xyz[1]))
    z.append(math.log10(xyz[2]))

# print(x)
# print(y)
# print(z)
fig=mplot.figure()
ax=fig.add_subplot(projection='3d')
ax.scatter(x,y,z)
ax.set_xlabel("V")
ax.set_ylabel("log(Reconf_time)")
mplot.show()
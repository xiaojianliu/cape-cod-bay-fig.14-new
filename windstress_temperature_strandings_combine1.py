# -*- coding: utf-8 -*-
"""
Created on Mon Jan 08 21:22:24 2018

@author: huimin
"""

import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.dates import date2num,DateFormatter,WeekdayLocator, MONDAY

year=2014
deep_temp=np.load('deep_temp.npy')
deep_time=np.load('deep_time.npy')
surf_temp=np.load('surf_temp.npy')
surf_time=np.load('surf_time.npy')
tuttle_time_num_u=np.load('tuttle_time_num_u.npy')
tuttle_time_num_v=np.load('tuttle_time_num_v.npy')
tuttle_time_u=np.load('tuttle_time_u.npy')
tuttle_time_v=np.load('tuttle_time_v.npy')
wind_time=np.load('wind_time_u.npy')
wind_u=np.load('wind_u.npy')
wind_v=np.load('wind_v.npy')

t1=date2num(tuttle_time_num_v.tolist())
t2=date2num(tuttle_time_num_u.tolist())
tt0=[]
tt1=[]
yy0=[]
yy1=[]
for b in np.arange(len(deep_time.tolist())):
    tt0.append((deep_time.tolist()[b]-datetime(2014,11,1)).days*24+(deep_time.tolist()[b]-datetime(2014,11,1)).seconds/float(60*60))
for b in np.arange(len(deep_time.tolist())):   
    tt1.append((deep_time.tolist()[b]-datetime(2014,11,1)).days*24+(deep_time.tolist()[b]-datetime(2014,11,1)).seconds/float(60*60))

ff0 = interpolate.interp1d(tt0, deep_temp.tolist(), kind='cubic')
ff1 = interpolate.interp1d(tt1, deep_temp.tolist(), kind='cubic')
nx = np.linspace(1, int(tt1[-1]), int(tt1[-1]))
tx=[]
for aa in np.arange(len(nx)):
    tx.append(datetime(2014,11,1)+timedelta(hours=nx[aa]))
    yy0.append((ff0(nx[aa]).tolist()+ff1(nx[aa]).tolist())/2.0)
width=0.4
fig=plt.figure(figsize=(15,12))
ax1=fig.add_subplot(211)
ax1.set_title(str(year)+' wind stickplot',fontsize=15)
ax1.set_xlabel("a",fontsize=13)
def stick_plot(time, u, v, **kw):    
    width = kw.pop('width', 0.002)    
    headwidth = kw.pop('headwidth', 2)
    headlength = kw.pop('headlength', 5)
    headaxislength = kw.pop('headaxislength', 5)
    angles = kw.pop('angles', 'uv')
    ax = kw.pop('ax', None)
    if angles != 'uv':
        raise AssertionError("Stickplot angles must be 'uv' so that"
                             "if *U*==*V* the angle of the arrow on"
                             "the plot is 45 degrees CCW from the *x*-axis.")
    time, u, v = map(np.asanyarray, (time, u, v))
    if not ax:
        ax = ax1
    q = ax.quiver(date2num(time), [[0]*len(time)], u, v,color='green',scale=6.,width=width, headwidth=headwidth,headlength=headlength, headaxislength=headaxislength)                 
    #qk = plt.quiverkey(q,0.6,0.8,0.3, r'$0.1 pa$',labelpos='E', fontproperties={'weight': 'bold','size':15},zorder=1)
    ax.axes.get_yaxis().set_visible(True)
    plt.xticks()
    #return qk
stick_plot(wind_time,wind_u,wind_v,color='green')
speed=[]
for a in np.arange(len(wind_u)):
    speed.append(np.sqrt(wind_u[a]**2+wind_v[a]**2))
ax1.bar(wind_time,speed,width=0.08,alpha=0.2,label="wind_stress",zorder=0)
ax1.set_ylabel('pa',fontsize=15)
mondays = WeekdayLocator(MONDAY)
ax1.xaxis.set_major_locator(mondays)
weekFormatter = DateFormatter('%b %d %Y')
ax1.xaxis_date()
ax1.xaxis_font = {'size':'13'}
ax1.xaxis.set_major_formatter(weekFormatter)
ax1.set_xlim(wind_time[0],wind_time[-24])
ax1.axes.get_xaxis().set_ticks([])
ax1.set_ylim(-max(speed)-0.1,max(speed)+0.1)
#########################################################

ax2=fig.add_subplot(212)
ax2.set_title(str(year)+' temperture vs strandings',fontsize=15)
ax2.set_xlabel("b",fontsize=13)
#############################
temp=10.7
aaax=2

index=0
ty=[]
for a in np.arange(aaax):
    ty.append(temp)

tx0=[wind_time[0]]

for a in np.arange(len(surf_temp)-1):
    if surf_temp[a]-temp>=0 and surf_temp[a+1]-temp<=0:
        index=a
        break

#index= np.argmin(np.abs(surf_temp2012-temp))
end_time=(surf_time[index]+timedelta(seconds=(surf_time[index+1]-surf_time[index]).seconds/2.0))
tx0.append(end_time)
ax2.plot(tx0,ty,'--',color='black')
ax2.plot([end_time,end_time],[0,temp],'--',color='black')
ax1.plot([end_time,end_time],[-1,1],'--',color='black')
print end_time
ax2.text(surf_time[index/3],10.4,'%s'%(temp))
ax2.text(surf_time[index-120],9.5,"""Nov %s %s"""%(end_time.day,end_time.year))

####################################3
bt,=ax2.plot(deep_time,deep_temp, label="bottom temperature (eMOLT)")
st,=ax2.plot(surf_time,surf_temp, label="surface temperature (FVCOM)")
ax21=ax2.twinx()

bar1=ax21.bar(t1,tuttle_time_v.tolist(),width,alpha=0.5,label="#strandings/day on Mid Cape")

bar2=ax21.bar(t2+width,tuttle_time_u.tolist(),width,alpha=0.5,color='red',label="#strandings/day on Outer Cape")
ax2.legend(handles=[bt,st,bar1,bar2],loc='upper right',fontsize=12)

ax2.set_ylim(7,14)
ax21.set_ylim(0,200)
ax2.set_ylabel("Degrees Celsius",fontsize=15)
ax21.set_ylabel("number",fontsize=15)
ax2.set_xlim(wind_time[0],wind_time[-1])
ax2.xaxis_font = {'size':'13'}
ax2.xaxis.set_major_locator(mondays)
ax2.xaxis_date()
ax2.xaxis.set_major_formatter(weekFormatter)
plt.xticks(fontsize=13)

plt.draw()
plt.savefig('windstickplot_temp_stranding_combine_'+str(year)+'.eps',format='eps',dpi=400,bbox_inches = "tight")
plt.show()

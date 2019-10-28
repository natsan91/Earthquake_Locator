# The following code deals with a well-known issue about basemap being outdated
# It involves basemap not pointing at the right environemental variables sometimes
# The issue is summarized here: https://github.com/conda-forge/basemap-feedstock/issues/30
# This workaround should work with a generic anaconda build
import os
cpath=os.getenv('CONDA_PREFIX')
os.environ["PROJ_LIB"]=cpath+"\Library\share"
# Import basemap
from mpl_toolkits.basemap import Basemap
# Import other relevant plotting utilities
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
from matplotlib.patches import Ellipse
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def makemap(stat_lats,stat_lons,stat_names,lonc,latc,lon_delt,lat_delt,
            itq=False,iterate=0,i_lons=0,i_lats=0):
    # Plots the map on a supplied axis
    # allows for plotting of stations via stat_ variables
    # lonc,latc are center of map with lon_delt,lat_delt radial distances
    # Optional arguments allow for plotting of iterated guesses at epicenter
    
    # Create map (static boundaries match random initial guess bounds)
    m = Basemap(llcrnrlon=lonc-lon_delt,llcrnrlat=latc-lat_delt,
                urcrnrlon=lonc+lon_delt,urcrnrlat=latc+lat_delt,resolution='l')

    # map cosmetics
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    m.drawlsmask(land_color='coral',ocean_color='aqua',grid=1.25)
    
    # add stations
    x, y = m(stat_lons, stat_lats)
    m.scatter(x, y, marker='D',color='m')
    # add labels for stations
    x2, y2 = (-20,5)
    for i in range(0,len(stat_lats)):
    	plt.annotate(stat_names[i], xy=(x[i], y[i]),  xycoords='data',
                    xytext=(x2, y2), textcoords='offset points',
                    color='m')
    
    # Plots all the guesses if this is part of the iteration
    if itq:
        if iterate==1: # first iteration complete, show initial guess and 
            x, y = m(i_lons[0],i_lats[0])
            m.scatter(x,y,marker='D',color='g')	
        elif iterate>1:
            x, y = m(i_lons[0],i_lats[0])
            m.scatter(x,y,marker='D',color='g')
            xx, yy = m(i_lons[1:iterate],i_lats[1:iterate])
            m.scatter(xx,yy,marker='D',color='r')
        xcurr, ycurr = m(i_lons[iterate],i_lats[iterate])
        m.scatter(xcurr,ycurr,marker='D',color='b')
        mytitle='After '+str(iterate)+' Iterations'
    else:
        mytitle='Map of seismic stations'
    plt.title(mytitle)
    
def final_map(lonc,latc,sem1,sem2,rot=0,time=0,tstd=0):
    # plots the final answer from the iteration on a tight axis around the 
    # epicentral location
    # additionally adds an error ellipse based on supplied values
    
    # Create map (static boundaries match random initial guess bounds)
    m = Basemap(llcrnrlon=lonc-3.,llcrnrlat=latc-2.,urcrnrlon=lonc+3.,
                urcrnrlat=latc+2.,resolution='l')

    # map cosmetics
    m.drawstates()
    m.drawcountries()
    m.drawcoastlines()
    m.drawlsmask(land_color='coral',ocean_color='aqua',grid=1.25)

    el=Ellipse((lonc,latc),sem1,sem2,rot,facecolor='b', zorder=10,alpha=0.4) 
    plt.gca().add_patch(el) 
    
    xcurr, ycurr = m(lonc,latc)
    m.scatter(xcurr,ycurr,marker='D',color='b')
    
    if (time*tstd)!=0:
        mylabel=r"t = {:.2f} $\pm$ {:.2f}s".format(time,tstd)
        plt.annotate(mylabel, xy=(xcurr, ycurr),  xycoords='data',
                     xytext=(-100., -15.), textcoords='offset points',
                     color='k')
        
        
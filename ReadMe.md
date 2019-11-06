# Earthquake Location Inference
Written by Nathan Sanford for Data Science 422 (inverse methods) at Northwestern in February 2017.

This short project takes data obtained from the Earthscope USArray system of earthquake detectors
and infers the hypocenter (or epicenter and origin time) of an earthquake from the times it took 
to reach a series of detectors. This process is sometimes called "triangulation," but is more 
properly called "multilateration" as more than three detectors are used. The data was obtained for 
the class by Dr. Suzan van der Lee, Professor in the Department of Earth and Planetary Sciences 
at NU and instructor for the course.

The data consists of arrival time data at a series of 12 seismic stations in the southeastern US.
The locations and elevations of the stations were also given and provided the basis for a least-
squares iteration process to find the hypocenter. The mathematical details are contained in 
[these notes](https://github.com/natsan91/Earthquake_Locator/blob/master/Earthquake_Inference.pdf "Earthquake_Inference.pdf"), 
but the main takeaway from this project for me was learning plotting 
tools in Python. I used [Basemap](https://matplotlib.org/basemap/), 
a Python mapping utility, to plot the iteration process on a map 
of the southeastern US in order to gain insight into the solution. In particular, a random initial 
guess for the epicenter sometimes does not converge and the geographical  distribution of the 
seismic stations provides insight as to why this is the case. An example of convergent iteration is
included seen here 

![Example Iteration](https://github.com/natsan91/Earthquake_Locator/blob/master/Example_iteration.png "Example with 5 iterations")

where the initial guess (green), intermediate iterates (red), and 
final iterate (blue) are shown on a map with the locations of the stations shown as well.

At the end of the iteration, which is achieved when the hypocenter changes are less than a 
prescribed tolerance, uncertainty information in the solution is displayed in the form of an error
ellipse. Output of a converged solution with an error ellipse is that is computed assuming that the input 
data have a standard error of 0.8s in each observation.

![Final answer](https://github.com/natsan91/Earthquake_Locator/blob/master/Example_zoomed.png "Final answer with error ellipse")

## A note on Basemap

Basemap is now deprecated in favor of another package called [cartopy](https://scitools.org.uk/cartopy/docs/latest/ ). 
Instead of updating this code to use cartopy I kept basemap but added a few workarounds for known issues. The code here 
using basemap is intended for use with anaconda3 and may not work with other flavors of python.
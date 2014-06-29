recat_arduino_python
=============

Python code that runs on the pc when used with the RECAT<br />
<br />
Matlab:
---------
absor.m					matlab that generates a transformation matrix given two sets of points<br />
absor\_wrapper.m	a way to easily run absor and tell it to read points from appropriate <br />
<br />
Python:
----------
cut\_script.py	script for cutting the path<br />
fydp\_common.py	common functions used between the scripts<br />
localization\_script.py generates the list of points in absolute space marked off during localization<br />
serial\_test.py	bunch of test commands<br />
<br />
Text files:
----------
ct\_coordinates (2).txt coordinates in ct frame used for localization<br />
ct\_coordinates.txt same file without the names for the points. used in matlab for now..<br />
arm\_dimensions.txt	lengths of the robot arm<br />
CutPathJONN.txt		list of ct coordinates with cut path<br />
tf\_matrix.txt		transformation matrix between ct coordinates and absolute.<br />
gantry\_coordinates.txt store the points that were drilled out. mainly for debugging.<br />

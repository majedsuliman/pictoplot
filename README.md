# pictoplot
DVD CNC Software 0.5 Beta

### Description
The Pic To Plot project came about from the need to automate the process of taking a picture and turning into GCode and sending to the DVD cnc machine
The project that build the cnc machine from DVD require manual steps to load the image into inkscape and use and the [MakerBot Unicorn G-Code Output for Inkscape](https://github.com/martymcguire/inkscape-unicorn) plugin to generate the GCode. 

This project performs the following steps to achieve this.

- Take the picture
- process the image using mkbitmap.exe
- convert the image to svg using potrace.exe
- Modify the SVG for better scaling to suit the plotter
- Convert the SVG to GCode using a combination of plugin and Inkscape extension python code

I have also added other features to make it useful such as GCode preview and a interface so you can see the picture.

For the hardware project see below.
### Hardware Project:

- [making an arduino based cnc plotter out of a dvd player](https://techcrunch.com/2016/11/30/making-an-arduino-based-cnc-plotter-out-of-a-dvd-player-is-as-easy-as-1-2-whats-arduino-again/)
- [mini-arduino-cnc](https://create.arduino.cc/projecthub/me_zain/mini-arduino-cnc-7e4e30)
- [How to Make Arduino Based Mini CNC Plotter Using DVD](http://www.instructables.com/id/How-to-Make-Arduino-Based-Mini-CNC-Plotter-Using-D/)

### Folder structure
|Folder|Description|
| ------ | ------ |
|bin | contains the any binary files|
|firmware | Used with the arduno to drive the plotter|
|img | images used with the pygame interface|
|inkscape | contins components for the converting of svg to gcode|
|pictoplot | contains the libary for transmitting and interface|
|test | contains test images and gcode|

### Usage
#### Headless Mode
Run as headless mode,this will perform all steps
['takepic','convtobmp','convtosvg','fixsvg','convtog','trans'].

This is the default mode

``` 
python pictoplot.py
or
python pictoplot.py -m 0 
```

#### Interface Mode
Use the interface this requres pygame to be installed
```
python pictoplot.py -m 1
```

#### Render GCode to diplay without plotting mode
Print the test gcode this 
```
python pictoplot.py -m 2
```

#### Print test image mode
Print the test image this prints a grid image located under test\photo.bmp
```
python pictoplot.py -m 3
```


#### Render GCode Mode
This will render the GCode result to screen
```
python pictoplot.py -m 4
```






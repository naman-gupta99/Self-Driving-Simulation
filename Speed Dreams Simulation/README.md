# Speed Dreams Simulation
  This part of the project aims at replicating the simulation done in the research paper :

  **I. Zubov, I. Afanasyev, A. Gabdullin, R. Mustafin, and I. Shimchik, “Autonomous Drifting Control in 3D Car Racing Simulator,” in 9th IEEE International Conference on Intelligent Systems 2018.**

  Source : [Link](https://www.researchgate.net/publication/328007272_Autonomous_Drifting_Control_in_3D_Car_Racing_Simulator)

## Overview
  The project aims at implementing a drift controller. We use Speed Dreams v2.1.1, to simulate the results of the controller.
  We use all-wheel drive electric Roborace Robocar on a custom race track with extremely wide boundaries to give liberty for the execution of drift. We apply mechanical bicycle model and simplified non-linear tire models to define tire parameters and two state equilibrium model to compute equilibrium points.

## System Setup
### Speed Dreams v 2.2.1
  First of all we need to install Speed Dreams v2.2.1.

  Installation Link : [Link](https://sourceforge.net/projects/speed-dreams/files/)

### Roborace Robocar Setup
  #### Installation
  Next we need to add the Roborace Robocar to our Speed Dreams directory.

  Package Link : [Link](https://drive.google.com/file/d/0B1UoOlZhZcoiR0Q1eU9abGFPTUk/view?usp=sharing)

  #### Modifications
  The default, Roborace Robocar is an electric motor car with 4WD (four-wheel drive). Since, the aim of this project is to Drift, we convert it to RWD (rear-wheel drive).

  To do this we need to exchange the file in the speed-dreams-2.2.1 directory :

  **/data/cars/models/Robocar/Robocar.xml**

  with the file **Robocar.xml** in the **Robocar** folder in this folder of the repository.

### Custom Track Generation
  #### Self Generation
  To generate your own custom track you can use the TORCS track-editor.

  TORCS track-editor : [Link](http://www.berniw.org/trb/download/trackeditor-0.6.2c.tar.bz2)

  #### Installation
  To reduce the effort we have provided the files that you will need to add our custom track.

  Just copy the **DriftCircle** folder in this folder of the repository in the following location in the speed-dreams-2.2.1 directory :

  **/data/tracks/cicuit**

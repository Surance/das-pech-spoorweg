# das-pech-spoorweg

## The Project

This project focuses on optimizing the rail schedule for trains in the Netherlands. The primary objective is to enhance the efficiency of the intercity train routes, connecting key stations the country. The task is to develop a high quality schedule of train routes that surpasses 89 of the most crucial stations with a maximum of 20 routes, each route not exceeding 180 minutes. 

The optimization function, denoted as K, plays a crucial role in evaluating the quality of the rail route map. The value of K is determined by factors such as the total travel time, the number of critical connections traversed, and the utilization of routes. 

Several algorithms have been developed to maximize the K value, and each algorithm provides a solution in the form of a set of routes tailored to meet the specified criteria for either of the outlined scenarios. 


## Getting Started

### Prerequisites

This code has been fully written in [Python3.9.18](https://www.python.org/downloads/). All neccessary packages to run the code successfully can be found in requirements.txt. These are easy to download using pip dmv. using the following instructions:

```
pip install -r requirements.txt
```

### Structure

The code is structures by the following folders:

- **/code**: contains all code from this project
  - **/code/algorithms**: contains code for the algorithms
  - **/code/classes**: contains the classes needed for the case
  - **/code/visualisation**: contains the code necessary for the visualisation of results
- **/data**: contains the different datafiles needed
- **/experiment**: contains the results from the code, saved per algorithm


### Use

An example can be run by calling the following:

```
python main.py
```

## Authors

* Jimmy T
* Josephine Woltering
* Marieke 

## Acknowledgments 

* Minor Artificial Intelligence UvA
* Tim Doolan 
* Wouter Vrielink
* Luka Zaitch
* Jacob Groot
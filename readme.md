This research designed and developed an autonomous Agent capable of catching free-falling packages in a store using Deep Q-Learning.

This project is managed with conda, you need to have conda installed on your computer to run this project

To run this project, you need to create and activate a conda environment with the project dependencies

Open a terminal on your computer and use the 4 step guide bellow

Step 1 : Create conda environment
conda create --name Gbemileke-Ajiboye-C2479785-Catching-Packages python=3.7

Step 2 : Activate 
conda activate Gbemileke-Ajiboye-C2479785-Catching-Packages


Step 3 : Install Dependencies on environment 
pip install torch torchvision matplotlib ipython pygame

Step 4 : Test the agent
python test-best-model.py

Note thet the program starts ploting after the first package miss

when you are done testing you can deactivete and remove the environment to freeup space on your computer in two Step

Step 1 : Deactivate the environment
conda deactivate

Step 2 : Remove the environment 
conda remove --name Gbemileke-Ajiboye-C2479785-Catching-Packages --all

A package store environment was implemented, the states and actions list for the environment was designed, and hyperparameters were experimented with to find the best combination of discount rate (gamma value) and negative reward to train a Deep Q-Learning agent. 

The agent was able to catch 16,429 packages and missed 65 packages out of 16,494 packages in 65 episodes during a 12-hour test recording an accuracy score of 99.606%
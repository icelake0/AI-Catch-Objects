This project is managed with conda, you need to have conda installed on your system to tun this project

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
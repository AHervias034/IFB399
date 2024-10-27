# AI Product Recommendation for CEOFFICE CONCEPTS

> **This repository contains the files used to create the demo AI Recommendation System for CEOFFICE CONCEPT
> by T023 for their IFB398 & IFB399 Capstone Project**

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running](#running)


---

## Introduction
This project was created in collaboration with CEOFFICE CONCEPTS to address their growing business needs and serves as a secondary deliverable for our client.

As CEOFFICE CONCEPTS continues to expand, the business aims to adopt more technology to support and accelerate growth. Our team was tasked with exploring how AI systems could enhance their operations and determining the potential benefits of early adoption. Through our analysis, we identified that an AI Recommendation System and an AI chatbot would be ideal starting points for integration, with each offering value in improving customer engagement and operational efficiency.

This repository specifically focuses on developing the AI Recommendation System, demonstrating its feasibility and functionality within CEOFFICE CONCEPTS. It provides a practical showcase of AI-driven recommendations while offering insights into the backend processes involved in building this AI capability.

## Directories
- **GUI:** Contains the GUI files to help in demonstrating the functionality
- **scripts:** Contains the main files for the AI model
- **test_scrappy:** Contains the web scrapper for getting the information of the recommended products

Further explanation will be in the directories.

## Installation
To install and set up the project, follow these steps:

1. **Clone the repository:**
   ```bash
   https://github.com/AHervias034/IFB399.git
   ```
2. **Download the dataset for the AI mode:**
   
   The download link below will download large files that needs to go in the following directory (scripts/data). Extract the files after downloading.

   ```bash
   https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/benchmark/0core/last_out_w_his/Home_and_Kitchen.train.csv.gz
   ```
   ```bash
   https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/benchmark/0core/last_out_w_his/Home_and_Kitchen.valid.csv.gz
   ```
   ```bash
   https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/benchmark/0core/last_out_w_his/Home_and_Kitchen.test.csv.gz
   ```
## Running
Its important the **step 2 in Installation** is done to run the system. To create necessary files to run the AI model.

The implementation uses paralleling techniques to help in speeding up the process of calculating/reading data. This may cause error or slow down the process for low end devices.

The system runs locally and requires an IDE, such as VSCode or PyCharm, to execute. Follow these steps to run it in PyCharm:

1. **Open the project in IDE.**

2. **Create the model files:**
   1. Run *run_model.py* in scripts directory. 
   2. It will ask for where to save the file enter: *model_log*
   3. It will ask for how many rows will be used for training: This one depends on your device I used *100000*. If the device can't try using *50000, 20000, 10000, 5000, 1000*
   4. It will ask for how many rows will be used for validation: This one depends on your device I used *10000*. If the device can't try using *5000, 2500, 1000, 500, 100*
   5. It will ask for how many rows will be used for test: This one depends on your device I used *10000*. If the device can't try using *5000, 2500, 1000, 500, 100*
   6. Should display **Model fitting completed.** if the code is run properly

3. **To run the GUI:**
   1. Open terminal in the IDE
   2. Change directory to GUI: **(cd .\GUI\)** 
   3. Enter *python app.py* in the terminal and run
   4. It should now be running locally in http://127.0.0.1:5000/

5. **Once the GUI is running the recommendation can be tested by entering the used ID's (These ID's are extracted from dataset):**
   1. AFKZENTNBQ7A7V7UXW5JJI6UGRYQ
   2. AGGZ357AO26RQZVRLGU4D4N52DZQ
   3. AGCI7FAH4GL5FI65HYLKWTMFZ2CQ
   4. AGKHLEW2SOWHNMFQIJGBECAF7INQ
   5. AGXVBIUFLFGMVLATYXHJYL4A5Q7Q
   6. AH6CATODIVPVUOJEWHRSRCSKAOHA
   7. AFSKPY37N3C43SOI5IEXEK5JSIYA
   8. AHXBL3QDWZGJYH7A5CMPFNUPMF7Q


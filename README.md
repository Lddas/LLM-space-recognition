# LLM-space-recognition

This repository is a copy of an Academic that we did (3 persons) for "Perception and Learning for Robots", an ETHZ course. I copied only the part that I did, which focus on the LLM's capacity of understanding and finding an itinerary in a real-world situation.
Please find here the final report of the project, and a picture of our final presentation poster.

[Spatial_Reasoning_from_LLM_for_Global_Navigation.pdf](https://github.com/user-attachments/files/17368274/Spatial_Reasoning_from_LLM_for_Global_Navigation.pdf)


![45ff1ebf-5cde-4eb1-8d77-d0e8a737ee67](https://github.com/user-attachments/assets/74487406-b740-4c5a-afe8-e8ced9ab8947)


## Room Navigation System

# Overview

The Room Navigation System is a web application designed to guide a user through a building to find a specific room. The system utilizes images captured from the surroundings and leverages an AI model to make navigation decisions based on visual input. This project demonstrates the capability of artificial intelligence to understand real-world environments. I did not upload the necessary pictures here.

Features

	•	Image-Based Navigation: The user provides three images (left, forward, right) of their surroundings, and the AI determines the best direction to proceed.
	•	Room Identification: The AI aims to find a designated room by processing the images and providing direction.
	•	Step-by-Step Guidance: The navigation happens step-by-step, allowing the user to retrace their steps if needed.
	•	OpenAI Integration: The system employs OpenAI’s models to analyze the images and make informed decisions.

Project Structure

	•	app.py: The main application file containing the Flask server and core logic for navigation.

	•	templates/index.html: HTML template for displaying images and navigation controls.
	•	static/: Directory for storing static files like images (if needed).
	•	requirements.txt: List of Python package dependencies required to run the project.

Getting Started

Prerequisites

	•	Python 3.x
	•	Required Libraries:
	•	Flask
	•	OpenAI

Usage

	1.	Run the main application file:
	2.	Open a web browser and navigate to http://127.0.0.1:5000/.
	3.	Follow the instructions in the web interface to upload images and guide the AI to find the desired room.

Customization

	•	The current setup is tailored for a specific building layout. If you wish to adapt the code for a different environment or layout, you may need to modify the possible_next dictionary and adjust image handling accordingly.


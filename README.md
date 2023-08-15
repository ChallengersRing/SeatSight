# SeatSight: An Open-Source Solution for Public Spaces

SeatSight is an innovative system designed to detect empty seats in public places using camera feeds and advanced computer vision techniques. This repository contains the source code and resources for the SeatSight project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

SeatSight aims to optimize seating availability and improve user experiences in various public spaces such as libraries, canteens, and waiting areas. By detecting empty chairs in real-time using camera feeds, this system provides valuable information about seat occupancy, allowing efficient resource management and a better user experience.

## Features

- Real-time detection of empty chairs and occupied chairs (when a person is detected to be sitting).
- Visualization of seat occupancy status on a user-friendly web-based interface.
- Integration with a pretrained YOLOv3 model for person and chair detection.
- Utilization of Django as the backend framework for data processing and management.
- Seamless integration of HTML, CSS, and JavaScript for the frontend, providing a dynamic and interactive user experience.
- Detailed logging and reporting of detection results.
- **Intersection over Union (IoU) Algorithm**: The system employs the IoU algorithm to precisely determine the occupancy of chairs. This algorithm evaluates the extent of overlap between the detected bounding boxes of persons and chairs, enabling accurate identification of whether a person is sitting on a chair or if the chair is vacant.


## Demo



## Getting Started

Follow these steps to set up and run the SeatSight project on your local environment.

### Prerequisites

- Python (3.7 or higher)
- Django (version 4.1.4, see [requirements.txt](requirements.txt))
- [Optional] YOLOv3 model weights and configuration files (can be downloaded from [link to model](https://github.com/ultralytics/yolov3))
- [Optional] Additional dependencies mentioned in [requirements.txt](requirements.txt)

### Installation

1. Clone this repository:

2. Install the required Python packages:


3. [Optional] Download the YOLOv3 model files (weights and configuration) and place them in the appropriate directory.

4. Run the Django development server:


The system should now be accessible at `http://localhost:8000/`.

## Usage

### Interacting with the Web Interface

1. **Access the System**: Open a web browser and navigate to the URL where the SeatSight system is running. The default address is usually `http://localhost:8000/` if running on the local development server.

2. **Homepage**: Upon accessing the system, you'll be presented with the homepage. This page displays an intuitive interface where you can view the seat occupancy status in real-time.

3. **Seat Status**: The system uses color-coded indicators to represent the status of each chair:

   - **Occupied**: The chairs where a person is detected sitting will be highlighted with a color indicating "Occupied."
   - **Vacant**: The vacant chairs will be highlighted with a different color, indicating "Vacant."

### Understanding Seat Occupancy Information

1. **Real-time Updates**: The system continuously analyzes the camera feed and updates the seat occupancy status in real-time.

2. **Occupancy Statistics**: On the web interface, you may find occupancy statistics that provide insights into the current state:
   - Total Chairs: The overall number of chairs in the monitored area.
   - Occupied Chairs: The count of chairs with detected occupants.
   - Vacant Chairs: The count of unoccupied chairs.

3. **Dynamic Visualization**: As individuals occupy or vacate chairs, the web interface dynamically updates the seat status, providing a visual representation of the changing occupancy patterns.

4. **Optimal Seating**: Use the provided information to make informed decisions about seating management in public places. Ensure optimal utilization of available chairs to enhance user comfort and resource efficiency.

Please note that the accuracy of seat detection may be influenced by environmental factors such as lighting conditions and camera angles. It's essential to keep these factors in mind while interpreting the seat occupancy information provided by the system.


## Contributing

We welcome contributions from the community! If you'd like to contribute to SeatSight, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.



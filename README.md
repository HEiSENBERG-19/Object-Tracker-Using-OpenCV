# Object Tracker with ROI Selection and Multiple Tracker Options

## Overview

This project is an advanced object tracker that allows you to select a Region of Interest (ROI) in a live camera feed and then track the object within that ROI using various tracking algorithms. The project is implemented using Python and OpenCV.

## Features

- **Live Camera Feed**: Displays the live feed from your camera.
- **ROI Selection**: Allows you to select a rectangular region of interest in the camera feed.
- **Multiple Tracker Options**: Supports KCF, CSRT, and MOSSE trackers.
- **Bounding Box**: Draws a bounding box around the tracked object.
- **FPS Display**: Displays the current frame rate (FPS) on the screen.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- A webcam or camera connected to your computer

## Installation

1. **Install Python**: Ensure that Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Create a Virtual Environment**: It's recommended to create a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Required Modules**: You can install the required modules using pip. Run the following commands:

   ```bash
   pip install numpy==2.1.1
   pip install opencv-contrib-python==4.10.0.84
   pip install opencv-python==4.10.0.84
   ```

5. **Install OpenCV Dependencies**:

   - **For Linux**:

     ```bash
     sudo apt-get install libopencv-dev python3-opencv
     ```

   - **For Windows and macOS**:
     - Windows: OpenCV should be installed via pip, as shown in step 4.
     - macOS: OpenCV should be installed via pip, as shown in step 4. If you encounter issues, you may need to install additional dependencies using Homebrew.

## How to Run

1. **Clone the Repository and navigate to the project directory**:

   ```bash
   git clone https://github.com/HEiSENBERG-19/Object-Tracker-Using-OpenCV.git
   cd <repository-directory>
   ```

2. **Run the Script**:

   ```bash
   python ObjectTracker.py
   ```

3. **Interact with the Program**:

   - The camera feed will open in a window.
   - Press `s` to select a region of interest (ROI). Click and drag your mouse to draw a rectangle around the area you want to select.
   - Press `spacebar` to confirm the selection.
   - The selected ROI will be highlighted with a blue bounding box, and the selected tracker will start tracking the object within that ROI.
   - Press `1`, `2`, or `3` to switch between KCF, CSRT, and MOSSE trackers respectively.
   - Press `q` to quit the program.

## Controls

- **`s`**: Select a region of interest (ROI) and start tracking.
- **`spacebar`**: Confirm the selection.
- **`1`**: Switch to KCF tracker.
- **`2`**: Switch to CSRT tracker.
- **`3`**: Switch to MOSSE tracker.
- **`q`**: Quit the program.

## Example

Here is a simple example of how the program works:

1. Run the script.
2. The camera feed will open.
3. Press `s` to select an ROI.
4. Draw a rectangle around the object you want to track.
5. Press `spacebar` to confirm the selection.
6. The bounding box will appear around the selected area, and the KCF tracker will start tracking the object.
7. Press `2` to switch to the CSRT tracker.
8. Press `q` to exit the program.

## Notes

- Ensure that your camera is properly connected and working before running the script.
- The program will automatically use the default camera (usually the built-in webcam). If you have multiple cameras, you may need to adjust the camera index in the `cv2.VideoCapture(0)` line.

## Troubleshooting

- **Camera Not Detected**: Ensure that your camera is properly connected and recognized by your operating system. You can check this in your system settings.
- **No ROI Selection**: Make sure you press `s` while the camera feed is active to select an ROI.
- **Tracking Issues**: If the tracking is not accurate, try selecting a more distinct and stationary object within the ROI.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.
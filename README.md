# Object Tracker

This Python script allows you to track objects in a video stream using OpenCV's object tracking algorithms. You can choose between different tracker types such as `CSRT` and `KCF`, and switch between them during runtime.

## Prerequisites

- Python 3.x
- OpenCV with contrib modules (for object tracking)

## Installation

### Step 1: Create a Virtual Environment

It is recommended to use a Python virtual environment to manage dependencies. Follow the steps below to create and activate a virtual environment.

1. Open a terminal or command prompt.

2. Navigate to the directory where your script is located.

3. Run the following command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

   This will create a virtual environment named `venv` in your project directory.

4. Activate the virtual environment:

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

### Step 2: Install Dependencies

After activating the virtual environment, install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 3: Running the Script

Once the environment is set up and dependencies are installed, you can run the script.

1. Use the following command to run the script:

   ```bash
   python object_tracker.py -v <path_to_video> -t <tracker_type> --width <video_width> --height <video_height>
   ```

   ### Example:
   ```bash
   python object_tracker.py
   ```

   ### Arguments:
   - `-v` or `--video`: (Optional) Path to the input video file. If not provided, the webcam will be used.
   - `-t` or `--tracker`: (Optional) The type of OpenCV tracker to use (`CSRT` or `KCF`). Default is `KCF`.
   - `--width`: (Optional) The width of the video frame. Default is `800`.
   - `--height`: (Optional) The height of the video frame. Default is `600`.

2. Interact with the video feed using the following keys:
   - `s`: Select a region of interest (ROI) to track.
   - `1` - `2`: Switch between available tracker types (e.g., `1` for `CSRT`, `2` for `KCF`).
   - `q`: Quit the program.

### Step 4: Deactivating the Virtual Environment

After you're done, you can deactivate the virtual environment by running:

```bash
deactivate
```

---

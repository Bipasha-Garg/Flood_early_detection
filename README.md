# Flood Early Warning System using OpenCV

This project is a prototype for a real-time flood and water level monitoring system using a standard webcam. It leverages computer vision techniques with OpenCV to detect the water surface level within a designated area. When the water rises above a predefined threshold, it triggers an audible alert. After the monitoring session, it performs a linear regression analysis on the collected data to model the rate of change and visualizes the results.


## Features

-   **Real-time Video Processing:** Captures and analyzes video feed directly from a webcam.
-   **Region of Interest (ROI) Selection:** Allows the user to specify the exact area to monitor, making the system adaptable to different camera placements.
-   **Water Level Detection:** Uses Canny Edge Detection and Hough Line Transform to identify the water's surface line.
-   **Audible Alerts:** Plays a sound alert when the water level surpasses a critical threshold.
-   **Data Logging:** Records time-series data of the water level (in pixels) to a text file (`Saved.txt`).
-   **Trend Analysis:** After monitoring, it fits a linear regression model to the data to analyze the trend (rate of rise/fall) and calculates the model's accuracy.
-   **Visualization:** Plots the measured water level against the predicted trend line for easy interpretation.

## How It Works

The system follows a clear pipeline from video capture to data analysis:

1.  **Camera Setup:** Initializes the webcam and allows the user to take a snapshot of the scene.
2.  **ROI Selection:** The user draws a rectangle on the snapshot to define the Region of Interest (ROI). All subsequent processing happens only within this rectangle. This is crucial for ignoring irrelevant parts of the video and improving performance.
3.  **Image Processing Loop:**
    -   The frame is cropped to the selected ROI.
    -   The color space is converted to HSV. While grayscale is often used, HSV can sometimes provide better contrast for edge detection under specific lighting conditions.
    -   **Canny Edge Detection** is applied to find sharp changes in intensity, which typically occur at the water's surface.
    -   **Probabilistic Hough Line Transform** (`HoughLinesP`) is used on the edge map to detect straight line segments.
4.  **Water Level Calculation:**
    -   The system filters for lines that are nearly horizontal (small slope), as this is characteristic of a water surface.
    -   It assumes the most prominent horizontal line is the water level.
    -   The height is calculated based on the line's vertical position (`y` coordinate) within the ROI. The formula `height = 150 - y_coordinate` indicates an inverted measurement, where a lower `y` value (higher in the frame) corresponds to a higher water level.
5.  **Alerting:**
    -   If the calculated pixel height exceeds a hardcoded threshold (`100`), an alert is triggered.
    -   The `playsound` library is used to play `sound.mp3`.
6.  **Data Logging and Analysis:**
    -   Throughout the session, each valid height measurement is stored.
    -   When the program is stopped (by pressing 'q' or via KeyboardInterrupt), the collected data points are saved to `Saved.txt`.
    -   A **Linear Regression** model from `scikit-learn` is trained on the data to find the best-fit straight line, representing the average rate of water level change.
    -   Key metrics like R-squared (coefficient of determination) and Mean Squared Error (MSE) are calculated to evaluate the model.
    -   Finally, `matplotlib` generates a plot showing the raw data points and the regression line.

## Requirements

You will need Python and the libraries mentioned below.

-   **`sound.mp3`**: Place an audio file named `sound.mp3` in the same directory as the Python script. You can use any `.mp3` file for the alert.

You can install the required Python packages using pip:

```bash
pip install opencv-python numpy playsound scikit-learn matplotlib
```

## How to Use

1.  **Clone the Repository / Save the Script:**
    Save the code as a Python file (e.g., `main.py`).

2.  **Install Dependencies:**
    Run the `pip install` command mentioned in the Requirements section.

3.  **Prepare the Alert Sound:**
    Make sure you have a `sound.mp3` file in the same folder as your script.

4.  **Run the Script:**
    Open a terminal or command prompt, navigate to the project directory, and run the script:
    ```bash
    python main.py
    ```

5.  **Select the ROI:**
    -   A window titled `"test"` will appear, showing a frame from your webcam.
    -   **Click and drag** with your mouse to draw a rectangle around the area where you want to monitor the water level (e.g., a container, a water mark on a wall).
    -   Press **ENTER** to confirm your selection.

6.  **Monitoring:**
    -   The script will now start monitoring in real-time.
    -   Two windows will be displayed:
        -   `Detected Line`: The live feed from your ROI with the detected water level line drawn in blue.
        -   `Edged Frame`: The output of the Canny edge detector.
    -   The console will print the detected height in pixels.

7.  **Stop the Program:**
    -   Press the **`q`** key while one of the OpenCV windows is active to stop the program gracefully.

## Expected Output

-   **Live Video Windows:** Real-time visualization of the detection process.
-   **Console Output:**
    -   Prints of the "Detected Height" during monitoring.
    -   An alert message when the water level rises.
    -   A summary of the regression analysis (R-squared, MSE, etc.) at the end.
-   **`Saved.txt`:** A comma-separated file containing the frame number and the corresponding measured height.
-   **Matplotlib Plot:** A graph titled "Water Level Over Time" showing the measured data and the linear trend line.

## Future Work

-   **Calibration:** Convert the pixel-based height measurement to real-world units (e.g., centimeters or inches) by calibrating the system with a known reference object.
-   **Robustness:** The current system only uses the *first* detected line. This could be improved by averaging the position of multiple detected horizontal lines or by implementing more advanced filtering to reject false positives.
-   **Alert Logic:** The current alert resets on every frame. A better approach would be to trigger the alert once and only reset it after the water level has receded significantly for a period of time.
-   **Advanced Alerts:** Integrate with services for SMS alerts or for email alerts for remote notifications.
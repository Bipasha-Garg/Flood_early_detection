import cv2
import math
import time
import numpy as np
from playsound import playsound  # Cross-platform sound module
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Capture video from camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

height = []
ret, frame = cap.read()
cv2.imwrite("testimage.jpg", frame)
im = cv2.imread("testimage.jpg")

# Select Region of Interest (ROI)
r = cv2.selectROI(img=im, windowName="test")

# Record start time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

prev_length = 0
alert_triggered = False
alert_threshold = 130
try:
    # Main loop
    while True:
        ret, frame = cap.read()
        if frame is None:
            break

        # Crop to ROI
        frame = frame[int(r[1]) : int(r[1] + r[3]), int(r[0]) : int(r[0] + r[2])]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        edges = cv2.Canny(gray, 100, 120)
        lines = cv2.HoughLinesP(edges, 1, math.pi / 180, 20, None, 20, 480)

        if lines is not None:
            dot1 = (lines[0][0][0], lines[0][0][1])
            dot2 = (lines[0][0][2], lines[0][0][3])
            dx = lines[0][0][2] - lines[0][0][0]
            if dx != 0:
                slope = (lines[0][0][3] - lines[0][0][1]) / dx
            else:
                slope = float("inf")

            if 0 <= slope <= 0.15:
                cv2.line(frame, dot1, dot2, (255, 0, 0), 3)
                length = 150 - lines[0][0][3]
                print("Detected Height:", length)
                height.append(length)

                # ✅ Alert condition if rise detected and alert is not triggered
                if length > 100 and not alert_triggered:
                    print("🚨 Water level rising! Playing alert sound.")
                    try:
                        playsound(
                            "sound.mp3"
                        )  # Ensure sound.mp3 exists in the working directory
                    except Exception as e:
                        print(f"Error playing sound: {e}")

                    alert_triggered = True

                # Reset alert when water level drops
                # if length < prev_length - alert_threshold and alert_triggered:
                #     alert_triggered = False  # Allow the alert to be triggered again
                alert_triggered = False
                prev_length = length

                cv2.imshow("Detected Line", frame)
                edged_frame = cv2.Canny(frame, 1, 100)
                cv2.imshow("Edged Frame", edged_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("\n⚠️ KeyboardInterrupt received.")
# Save data to text file
x = []
y = []
file = open("Saved.txt", "a")
for i in range(len(height)):
    x.append(i)
    y.append(height[i])
    file.write(str(x[i]) + "," + str(y[i]) + "\n")
file.close()

# Convert to NumPy arrays
X = np.array(x).reshape(-1, 1)
Y = np.array(y).reshape(-1, 1)

# Fit linear regression model
model = LinearRegression().fit(X, Y)
r_sq = model.score(X, Y)
y_pred = model.predict(X)

# Display results
print("Predicted Response:\n", y_pred)
print("Start Time:", current_time)
print("Coefficient of Determination:", r_sq)
print("Intercept:", model.intercept_)
accuracy = mean_squared_error(Y, y_pred)
print("Accuracy (MSE):", accuracy)
t = time.localtime()
current_time2 = time.strftime("%H:%M:%S", t)
print("Stop Time:", current_time2)

# Plot results
plt.plot(X, Y, ".", color="black", label="Measured")
plt.plot(X, y_pred, color="blue", label="Predicted")
plt.title("Water Level Over Time")
plt.xlabel("Time (frames)")
plt.ylabel("Height (pixels)")
plt.legend()
plt.show()

# Cleanup
cap.release()
cv2.destroyAllWindows()

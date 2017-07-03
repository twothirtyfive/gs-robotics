This is the lab 4 submission for Robotics Dream Team of General Studies.
Members: Julian Kocher (jk3813), Najlaa Bouras (nb2749), Michael Falkenstein (maf2233)

Youtube link for video: https://youtu.be/tht7e58j8Yg

NOTE:
  -we used X11 over SSH in order to display the initial snapshot (for identifying the color being tracked) using the -Y flag
  -the use of our driver.py file requires our custom control.py, which is included in the zip file
  -the code also requires the most up-to-date version of gopigo.py, found on the GoPiGo github

We followed the general order recommended for this lab, and it was helpful. We used OpenCV extensively.
Certain particulars of the behavior of our robot are:
  Sometimes, upon taking a picture, the jpg file is corrupted and a portion of the image will be missing a color. Unfortunately, the color of our target shares the same range of HSV values, and the robot occasionally backs up momentarily as it believes the target is very close. Reflashing or replacing the memory card may remove this error, or it may from the camera.
  If the target begins to move out of frame, the robot will halt its current movement and turn to face the target. This is to ensure that the robot can always maintain sight of the target.

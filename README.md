Lab 1 Submission for Robotics Dream Team of General Studies
Members: Julian Kocher (jk3813), Najlaa Bouras (nb2749), Michael Falkenstein (maf2233)

Code requires the included control.py, as it has been modified from the original.

Part 1: Code implementation found in lab1_1.py.
Part 2: Code implementation found in HW1-2.py. Robot dances randomly for 20 seconds.
Part 3: Code implementation found in HW1-3.py. Setting up with the sensor 5cm from the target, its takes a distance reading, backs up 25cm, takes a reading, backs up 30cm and takes a final reading.
    Averaged distance reading at 5cm: 4.0
    Averaged distance reading at 30cm: 27.2
    Averaged distance reading at 60cm: 62.8
Part 4: Code implementation found in lab1_4.py.
Part 5: Code implementation found in HW1-5.py. The robot takes 180 degrees of readings with 15 degree increments. Upon returning to its original position, it reorients itself towards the obstacle and performs another rough search. If the obstacle is not found, it rotates 90 degrees and tries again. Once the obstacle is verified, it performs a fine search (90 degrees with 5 degree increments) and approaches the obstacle. It stops 20cm from the obstacle.

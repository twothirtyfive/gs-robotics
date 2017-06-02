Lab 1 Submission for Robotics Dream Team of General Studies
Members: Julian Kocher (jk3813),

Part 1: Code implementation found in lab1_1.py.

Part 2: Code implementation found in HW1-2.py. Video included.
Part 3: Code implementation found in HW1-3.py.
    Averaged distance reading at 5cm: 4.0
    Averaged distance reading at 30cm: 27.2
    Averaged distance reading at 60cm: 62.8
Part 4: Code implementation found in HW1-4.py.
    Target: Thin book called Polygon Mesh Processing
    At first I thought there was a possibility the cone would be ~12 degrees.
    Accordingly, I designed the code to search for a book every 5 degrees, turning to the left.
    Once the book was found, degree ALPHA was saved.
    It continued to the left 1 degree at a time until it could no longer sense the book.
    Degree MAX was saved as the previous degree. Remington then turned it's head to degree (alpha-1).
    Then it continuously turned its head to the right(subtracting degrees) 
    until it could no longer sense the book. Current degree + 1 is then registered as degree MIN.
    Running this code several times with Remington with a thin book around 64 away gave me
    MAX-MIN = 49-degree cone.
Part 5: Code implementation found in HW1-5.py.

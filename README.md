🧭 Topographic Calculator App – Tkinter

📖 Overview
  This desktop application was developed as a university project to facilitate common topographic calculations. It was built using Python with Tkinter as the graphical interface library. The program is designed to help students, surveyors, and professionals       
  perform essential coordinate geometry and topographic computations in a simple and interactive way.

It offers a clear structure and modular design, enabling users to input data and receive immediate calculations with visual and numerical outputs.

🚀 Features
The application provides the following tools:

1. Azimuth Calculation
  Calculate the azimuth (bearing) between two given points, representing the angle from the north in a clockwise direction.

  Inputs: Coordinates of Point A and Point B (X, Y)

  Output: Azimuth in degrees

2. Coordinate Calculation
  Compute the coordinates of a new point based on an origin, azimuth, and distance.

  Inputs: Known point (X, Y), azimuth angle, and horizontal distance

  Output: Destination coordinates (X, Y)

3. Working Angle and Height Difference (Δh)
  Calculate both the slope angle and the vertical height difference between two points.

  Inputs: Horizontal distance and zenith angle

  Output: Working angle and height difference

4. Minimum Distance from a Point to a Line
  Determine the shortest distance from an external point to a straight line defined by two points.

  Inputs: Coordinates of the line points (A and B) and the external point (C)

  Output: Minimum distance from point C to line AB

5. Line Intersection
  Find the intersection point of two lines, each defined by two coordinates.

  Inputs: Coordinates of four points (two per line)

  Output: Intersection point (X, Y), or a message if lines are parallel

6. Polygon Area (5 Vertices)
  Calculate the area of a polygon given five (X, Y) vertices using the Shoelace formula.

  Inputs: Coordinates of five points

  Output: Area in square units

🖥️ How to Use
  🔐 Login
  When the application is launched, it begins with a login screen. You can modify the allowed users or remove the login entirely in the LoginWindow class.

📋 Interface Navigation
  A sidebar allows you to navigate between features.

  Each section provides labeled input fields and a clear "Calculate" button.

  Result labels show output with proper formatting.

📤 Data Entry
  Only numerical input is accepted. If the user enters invalid data, an error message will be displayed using messagebox.

  Units are assumed to be consistent (meters, degrees, etc.), and should match throughout each calculation.

🧱 Technical Structure
  Language: Python 3.13.3

  UI Library: Tkinter
  
  Error Handling: messagebox alerts

  OOP Design: Classes for login and main application interface

Core Classes:

  LoginWindow: Simple authentication window

  MainApp: Handles sidebar navigation and calculation frames

  Methods per feature: Each tool is self-contained in its own function with clearly labeled inputs and outputs

💡 Example Use Case
  Suppose you are given the coordinates of two topographic points (N, E) and need to:

  Calculate the azimuth from point A to B.

  Determine a new point 150 meters away from A at that azimuth.

  Measure the height difference from a zenith angle.

  Confirm the point lies near an intended line.

  Calculate the area of a defined boundary using 5 known points.

  All of the above can be executed within this application—quickly and intuitively.

📌 Project Scope and Future Enhancements
  This project was developed as part of a university course in surveying and geomatics. It currently includes the most common manual calculations required in field reports and lab work.

Potential Extensions:
  Import/Export data from .csv or .txt

  Visual plotting using matplotlib

  Support for more than 5 polygon vertices

  Conversion tools between UTM, geographic, and Cartesian coordinates

  Elevation profiles and 3D terrain visualizations

📷 Screenshots
![ss](https://github.com/user-attachments/assets/14fa61cb-8ffb-433a-8576-7c28c0abdbf6)


📚 Requirements
  Python 3.13.3


No external libraries are needed beyond the standard library

To run the program:

  bash
  Copy
  Edit
  coordenadas-toolkit.py
Make sure all .py files are in the same directory.

👤 Author
Developed by [Your Name]
As part of a coursework project in [Name of University] — [Department/Course Title]
Year: 2025

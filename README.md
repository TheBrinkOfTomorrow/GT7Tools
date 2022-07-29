# GT7Tools
Python toolset for capturing and processing data from GT 7

<B>GT7SumulatorPY.py

Usage: Enter "s" to start date capture, "h" to halt logging, "q" to quit, "help" for more options.


From in-program help message:

Usage:  Type the following (plus <Return>):
  - s	:      (Re)Starts data packet capture
  - h	:      Halts data packet capture
  - q	:      Quits the application
  - r	:      Resets existing data already captured
  - o :	    Saves the data captured to a binary file (name=./test-data.gt7)
  - z	:      Loads the data (previously captured and saved) from a binary file (name=./test-data.gt7)
  - g	:      Graphs the the data loaded from binary file (throttle, brake, speed, RPM)
  - csv	:    Saves the captured data to a .csv file (name=gt7-datalog-<date>-<time>.csv)
  - csvpos : Saves the captured POSITION data to a .csv file (name=gt7-datalog-<date>-<time>.csv)

 
Example graph:
  
  ![HighSpeedRing-2022-07-28](https://user-images.githubusercontent.com/36106138/181679590-880f3002-f966-43cf-966a-a2606dd459c3.jpg)

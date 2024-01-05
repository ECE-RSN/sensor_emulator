# RSN

This serial emulator (and included data files) will behave like two of the sensors we use in EECE 5554. It will write data strings (either NMEA strings or VectorNav strings) to a specified serial port, thus "emulating" the sensor's output. The emulator will help you write drivers and test your publisher nodes without accessing the hardware. This way, we can be as efficient with our use of the actual sensors (GPS pucks, VectorNav units) as possible. 

The emulator has been tested with Python 3.8, written by Jagapreet Singh Nir, and updated by Kris Dorsey.

To get the serial emulator, clone this repository with:
$ git clone https://github.com/ECE-RSN-Staff/sensor_emulator/

The emulator has a dependency on the pyserial module (https://pypi.org/project/pyserial/), so you will need to first get that by: 
$ pip3 install pyserial

After you have cloned the repository and gotten the pyserial module, you can run the emulator. 

$ python3 serial_emulator.py -h 

will give you help options to run the script and 

$ python3 serial_emulator.py --file file --sample_time time

where file is the datafile you want to write to the serial port, and time is the sampling time at which you want to write (in Hz). For example, if I wanted to read the data in file GPS_Chicago.txt from the serial port, my command would be 

$ python3 serial_emulator.py --file GPS_Chicago.txt --sample_time 1

The emulator will print the pseduo device address /dev/pts/N to the terminal, where N will be some system-generated integer. You can use this pseudo-address to test your driver or see output on minicom with 
    minicom -D /dev/pts/N

where N is the actual number that is printed to the terminal when you start the emulator.

#####Information only for VectorNav!#####

The IMU also has a modifiable sampling time that you can use to test out your command for writing a change in sampling time to the sensor's registry. For example: 

$ python serial_emulator.py --file imu_data.txt -V appropriate-VectorNav-string

will "write" the string appropriate-VectorNav-string to the emulated VectorNav registry. If you have provided the correct string, it will change the sampling rate.


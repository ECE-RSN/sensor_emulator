# RSN

This serial emulator (and included data files) will behave like two of the sensors we use in EECE 5554. It will write data (either NMEA strings or VectorNav strings) to a specified serial port, thus "emulating" the sensor's output. The emulator will help you write drivers and test your publisher nodes without accessing the hardware. This way, we can be as efficient with our use of the actual sensors (GPS pucks, RTK hardware, VectorNav units) as possible. 

The emulator has been tested with Python 3.8, written by Jagapreet Singh Nir, and updated by Kris Dorsey.

To get the serial emulator, clone this repository with:
$ git clone https://github.com/ECE-RSN/sensor_emulator/

The emulator has a dependency on the pyserial module (https://pypi.org/project/pyserial/), so you will need to first get that by: 
$ pip3 install pyserial

After you have cloned the repository and gotten the pyserial module, you can run the emulator. 

$ python3 serial_emulator.py -h 

will give you help options to run the script and 

$ python3 serial_emulator.py --file file --device_type device --loop loop behavior --VN_reg write_reg_command

where file is the datafile you want to write to the serial port, device_type being the type of device you want to emulate, and loop_behavior is whether you want the emulator to loop through the file or quit once it has reached the end of the file. For example, if I wanted to read the data in file GPS_Chicago.txt once from the serial port, my command would be 

$ python3 serial_emulator.py --file GPS_Chicago.txt --device_type gps --loop "no"

and if I wanted to loop through the data, the line would be 

$ python3 serial_emulator.py --file GPS_Chicago.txt --device_type gps --loop "yes"

Defaults: Setting the device_type to gps or rtk will set the sampling rate to the default for that device.Setting the device_type to imu sets the default to 200 Hz. No loop flag will result in looping behavior so the data is streamed until the user quits the process with command-C

The emulator will print the pseudo device address /dev/pts/N to the terminal, where N will be some system-generated integer. You can use this pseudo-address to test your driver or see output on minicom with 
    minicom -D /dev/pts/N

where N is the actual number that is printed to the terminal when you start the emulator.

#####Information only for VectorNav!#####

The IMU also has a modifiable sampling time that you can use to test out your command for writing a change in sampling time to the sensor's registry. For example: 

$ python serial_emulator.py --file imu_data.txt --device_type imu -V appropriate-VectorNav-string

will "write" the appropriate-VectorNav command to the emulated VectorNav registry. If you have provided the correct command, it will change the sampling rate. Please include this command as exactly what you would write to the VN to have it change the rate.


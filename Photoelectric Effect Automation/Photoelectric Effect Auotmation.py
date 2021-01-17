
# %%

from matplotlib.animation import FuncAnimation  # for real time display
import matplotlib.pyplot as plt
import numpy as np
# The following line, 'import visa', raises an error, "AttributeError: module 'visa' has no attribute 'ResourceManager'."
# It needs to be 'import pyvisa as visa' instead.
# This issue is discussed on Github discussion page "https://github.com/pyvisa/pyvisa/issues/392"
#import visa  #here if using usb connection with vxi-11 or ni-visa
import pyvisa as visa


#from serial import SerialException
rm = visa.ResourceManager()
print("Here are the resources in use: ")
print(rm.list_resources())
resources = rm.list_resources()

# Here are the device names of the three instruments connected via USB (865A), or USB serial converter:

voltmeter = '5491B  Multimeter,Ver1.4.14.06.18,124E16150' # voltmeter for measuring stopping voltage
ammeter = '5491B  Multimeter,Ver1.4.14.06.18,124D17150' # "ammeter" that measures the voltage equivalent photocurrent

#%%
#Determine which resources are valid by issuing *IDN? query to all devices:

return_list=[]
print("Opening them in turn and asking who they are: ")
for i in resources:
    print("Resource: ",i)
    try:
        res_list = rm.open_resource(i)
        res_list.read_termination = '\n'
        res_list.write_termination = '\n'
        res_list.baud_rate = 38400
        return_str = res_list.query('*IDN?') # checks the name of the device
        if return_str == voltmeter:
            volts = res_list
        elif return_str == ammeter:
            amps = res_list
        return_list.append(return_str)
    except:
        continue

try:
    print("Voltmeter: ", volts)
except NameError:
    NameError("Could not find voltmeter")

try:
    print("Ammeter: ", amps)
except NameError:
    NameError("Could not find ammeter")

#%%

fig, ax = plt.subplots()
plt.xlabel("Stopping Voltage (V)")
plt.ylabel("Photocurrent (A)")
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

count = 0
end_count = 50 # how many times data will be collected

def update():

    if count < end_count:
        voltage = float(volts.query("FETC?"))
        amperage = float(amps.query("FETC?"))
        xdata.append(voltage)
        ydata.append(amperage)
        ln.set_data(xdata, ydata)
        ax.relim() 
        ax.autoscale_view()
        count += 1

        return ln,

ani = FuncAnimation(fig, update)
plt.show()


#!/usr/bin/env python3
# license removed for brevity

# Import for ROS
import rospy
from std_msgs.msg import Float64MultiArray

# Import for ADC
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def talker():
	# Create the I2C bus
	i2c = busio.I2C(board.SCL, board.SDA)

	# Create the ADC object using the I2C bus
	ads1 = ADS.ADS1115(i2c)

	# Create single-ended input on channel 0
	chan1 = AnalogIn(ads1, ADS.P0)
	chan2 = AnalogIn(ads1, ADS.P1)
	
	# Publish value and voltage values
	pub = rospy.Publisher('/adcros_topic', Float64MultiArray, queue_size=10)
	rospy.init_node('adc_publisher_node', anonymous=True)
	rate = rospy.Rate(100) # 100hz
	
	voltage_value = Float64MultiArray()

	while not rospy.is_shutdown():
		voltage_value.data = [chan1.voltage, chan2.voltage]
		pub.publish(voltage_value)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

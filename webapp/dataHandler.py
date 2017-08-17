#data handler object that reads bits from the data.txt file in the gate directory and 

import time
import threading
from datetime import datetime

class dataHandler(object):

	data = None
	count = None
	timeString = None
	start_time = datetime.now()

	def __init__(self):
		self._lock = threading.Lock()
		self._data_callback = None
		self._count_callback = None
		self._data_thread = threading.Thread(target=self._update_data)
		self._data_thread.daemon = True
		self._data_thread.start()

	def _update_data(self):
		while True:
#		for i in range(0,1000):
			with self._lock:
				self.timeString = '{}'.format(datetime.now() - self.start_time)
				f = open('/home/pi/slimgateProto/gate/data.txt')
				self.data = str(f.readline())
				self.count = str(f.readline())
				f.close()
				if self._data_callback is not None:
					self._data_callback(self.data, self.count, self.timeString)
			time.sleep(0.1)

	def on_data_change(self, callback):
		self._data_callback = callback

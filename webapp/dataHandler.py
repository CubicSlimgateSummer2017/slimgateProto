import time
import threading

class dataHandler(object):

	data = None

	def __init__(self):
#		data = 0
		self._lock = threading.Lock()
		self._data_callback = None
		self._data_thread = threading.Thread(target=self._update_data)
		self._data_thread.daemon = True
		self._data_thread.start()

	def _update_data(self):
		while True:
#		for i in range(0,1000):
			with self._lock:
#				print("testing repeated outputs, data = " + str(data))
				f = open('/home/pi/slimgateProto/gate/data.txt')
				self.data = str(f.readline())
				f.close()
				#self.data += 1
				if self._data_callback is not None:
					self._data_callback(self.data)
			time.sleep(0.1)

	
	def on_data_change(self, callback):
		self._data_callback = callback

import time
import threading

class slimgate(object):

	count = 0

	def __init__(self):
#		count = 0
		self._lock = threading.Lock()
		self._count_callback = None
		self._count_thread = threading.Thread(target=self._update_count)
		self._count_thread.daemon = True
		self._count_thread.start()

	def _update_count(self):
		for i in range(0,1000):
			with self._lock:
#				print("testing repeated outputs, count = " + str(count))
				self.count += 1
				if self._count_callback is not None:
					self._count_callback(self.count)
			time.sleep(1)

	
	def on_count_change(self, callback):
		self._count_callback = callback

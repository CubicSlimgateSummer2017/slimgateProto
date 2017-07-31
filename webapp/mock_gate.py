import time
import threading

count = 0

class mockGate(object):
	def __init__(self):
		self._lock = threading.Lock()
		self._state_thread = threading.Thread(target=self._update_state)
		self._state_thread.daemon = True
		self._state_thread.start()

	def _update_state(self):
		for i in range(0,1000):
			with self._lock:
				print("testing repeated outputs, count = " + str(count))
				count += 1
			time.sleep(1)

	
	def read_gate(self):
		return count

import queue
import threading
from gpm import Models


class Automation:
    def __init__(self):
        """Cấu hình GPM"""
        self.gpm = Models(
            API_URL= 'http://127.0.0.1:19995',
            x= 700,
            y=1200
        )

        """Tỉ lệ khung hình"""
        self.dpi  = 0.7
        """Sắp xếp cửa sổ """
        self.panel = 6
    




Thread = 5
def setup():
    profile = Models().profile_list()
    """Hàng đợi"""
    TaskQueue =  queue.Queue()
    for _ in profile:
        """Put profile vào hàng đợi"""
        TaskQueue.put(_)
    




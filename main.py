import queue
import threading
from gpm import Models
import functools
import time
import re
from keys import KeysProfile
from lib import *


def retry(loop=5, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(loop):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(delay)
        return wrapper
    return decorator


class Automation:
    def __init__(self , *_args):
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
        self.queue : queue.Queue = _args[1]
        self.x         = _args[0]
        self.thread_id = _args[2]
        self.run()
    def run(self ):
        while not self.queue.empty():
            """Lấy data từ Queue"""
            self.profile : KeysProfile = self.queue.get(timeout=1)
            self.driver  = self.chrome()

            """Phần này sẽ dùng để chạy các Task - Mọi người tự code thêm"""
            self.driver.get('https://accounts.google.com/')
            self.login()

            """/END"""
            """Gửi tín hiệu done"""
            
            self.gpm.close_v3(self.profile['id'])
            self.queue.task_done()
        # print("done")
    @retry(loop=5, delay=1)
    def login(self):
        if re.search('myaccount.' , self.driver.current_url):
            """Đã đăng nhập"""
            return
        
        time.sleep(3)
        self.email , self.password , self.two_factor =  ''.split('|')
        """Login Task Gmail"""
        identifier = WebDriverWait(
            self.driver,
            60
        ).until(EC.element_to_be_clickable((By.NAME ,'identifier')))

        if identifier:
            identifier.send_keys(self.email)
            identifier.send_keys(Keys.ENTER)

        Passwd = WebDriverWait(
            self.driver,
            60
        ).until(EC.element_to_be_clickable((By.NAME ,'Passwd')))
        Passwd.send_keys(self.password)
        Passwd.send_keys(Keys.ENTER)
    @retry(loop=5 , delay=1)
    def chrome(self):
        profile = self.gpm.start_v3(
            profile_id=self.profile['id'],
            x=self.x,
            dpi=self.dpi,
            toa_x=self.panel
        )

        if profile.get('message') == 'ALREADY_OPEN':
            self.gpm.close_v3(self.profile['id'])

        options = Options()

        """Path open profile"""
        service = Service(executable_path=profile['data']['driver_path'])
        self.debugger_address =  profile['data']['remote_debugging_address']
        options.debugger_address = self.debugger_address
        return webdriver.Chrome(
            service = service,
            options=options
        )

"""Cài đặt tiến trình Multi"""
max_thread = 2
TaskQueue =  queue.Queue()
def setup():
    global TaskQueue
    profile = Models().profile_list()
    """Hàng đợi"""
    for _ in profile:
        """Put profile vào hàng đợi"""
        TaskQueue.put(_)

if __name__ == '__main__':
    threads = []
    setup()

    for index in range(max_thread):
        """Tham số"""
        _args = (
            index  % TaskQueue.qsize() , # panel 
            TaskQueue ,# Queue data
            index + 1
        )
        thread = threading.Thread(target=Automation , args=_args)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
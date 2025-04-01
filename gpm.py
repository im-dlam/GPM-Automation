import requests
import random
from time import sleep
import json

class Models:
    def __init__(self, API_URL='http://127.0.0.1:19995', x=500, y=800, panel_x=0, panel_y=0) -> None:
        self.host_gpm = API_URL
        self.size_x = x
        self.size_y = y
        self.panel_x = panel_x
        self.panel_y = panel_y

    def start(self, profile_id, x, dpi, toa_x):
        pos_x = (x % toa_x) * self.size_x - self.panel_x * (x % toa_x) if (x % toa_x) != 0 else (x % toa_x) * self.size_x
        pos_y = (x // toa_x) * self.size_y - self.panel_y * (x // toa_x)
        # --ash-no-nudges: Tránh các cú huých "giáo dục người dùng" bong bóng màu xanh lam (ví dụ: "... mang đến cho trình duyệt của bạn một giao diện mới", Trình tiết kiệm bộ nhớ)
        # --mute-audio: Tắt tiếng mọi âm thanh
        # --disable-dev-shm-usage tắt sử dụng bộ nhớ tạm thời
        # http://127.0.0.1:19995//api/v3/profiles/start/bcc5cff4-76f6-46ea-991a-f751974a4a86?win_size=500,800&?win_scale=0.3
        arg = f'{self.host_gpm}/api/v3/profiles/start/{profile_id}?window-size={self.size_x},{self.size_y}&force-device-scale-factor={dpi}&window-position={pos_x},{pos_y}'
        call_open = requests.get(arg).json()
        return call_open
    
    def create(self, proxie='null', group='All'):
        name = str(random.randint(100000, 999999))
        arg = f'{self.host_gpm}/v2/create?name={name}&group={group}&proxy={proxie}'
        try:
            return requests.get(arg).json()['profile_id']
        except: return False

    def close(self, profile_id):
        return requests.get(f'{self.host_gpm}/v2/stop?profile_id={profile_id}')

    def profile_list(self):
        call_list_profile = requests.get(f'{self.host_gpm}/v2/profiles?per_page=1000000').json()
        return call_list_profile
    
    def update(self, profile_id, proxy):
        call_update = requests.get(f'{self.host_gpm}/v2/update?id={profile_id}&proxy={proxy}').text
     
    def delete(self, profile_id):
        call_dele = requests.get(f"{self.host_gpm}/v2/delete?profile_id={profile_id}")

    def group_v3(self):
        list_gr = requests.get(f'{self.host_gpm}/api/v3/groups').json()
        return list_gr
    def profile_list_v3(self, id_gr=1):
        list_group = requests.get(f'{self.host_gpm}/api/v3/profiles?group_id={id_gr}&per_page=1000000&sort=1').json()
        return list_group
    def start_v3(self, profile_id, x, dpi, toa_x):
        pos_x = (x % toa_x) * self.size_x - self.panel_x * (x % toa_x) if (x % toa_x) != 0 else (x % toa_x) * self.size_x
        pos_y = (x // toa_x) * self.size_y - self.panel_y * (x // toa_x)
        
        # http://127.0.0.1:19995/api/v3/profiles/start/{profile_id}?win_size=500,800&win_scale=0.3&win_pos=0,0
        arg = f'{self.host_gpm}/api/v3/profiles/start/{profile_id}?win_size={self.size_x},{self.size_y}&win_scale={dpi}&win_pos={pos_x},{pos_y}'
        call_open = requests.get(arg).json()
        return call_open
    def profile_info(self, profile_id):
        for _ in range(5):
            try: return requests.get(f'{self.host_gpm}/api/v3/profiles/{profile_id}').json()
            except: sleep(5)
        return False
        
    def create_v3(self, proxie='', group='All'):
        name = str(random.randint(100000, 999999))
        arg = f'{self.host_gpm}/api/v3/profiles/create'
        json_data = {
            "profile_name" : name,
            "group_name" : group,
            "raw_proxy" : proxie
        }
        data = json.dumps(json_data)
        try:
            return requests.post(arg, data).json()
        except: return False
    def update_v3(self, profile_id, proxie):
        json_data = {
            "raw_proxy" : proxie,
        }
        data = json.dumps(json_data)
        update = requests.post(f'{self.host_gpm}/api/v3/profiles/update/{profile_id}', data).json()
        return update
    def close_v3(self, profile_id):
        requests.get(f'{self.host_gpm}/api/v3/profiles/close/{profile_id}')

import psutil
import requests
from datetime import datetime

from ...xlog import xlogger


class Check():
    def __init__(self, request_name_list={}):
        self.request_name_list = request_name_list
        self.cpu_percent = 0
        self.memory_percent = 0
        self.disk_percent = 0
        self.baidu = 404
        self.google = 404
        self.process_name_list = []
        self.process_status_list = []
        self.user_list =[]
        self.run_all_check()

    def run_all_check(self):
        self.get_performance_check()
        self.get_network_check()
        self.get_process_status(self.request_name_list)
        self.get_users_check()

    async def get_check_info(self):
        self.run_all_check()
        putline = []

        putline.append("--Performance--\n[Cpu] {}%\n[Memory] {}%\n[Disk] {}%\n--Network--\n[Baidu] {}\n[Google] {}".format(self.cpu_percent, self.memory_percent, self.disk_percent, self.baidu, self.google))
        
        if self.process_name_list:
            putline.append("--Process--")
            for name, status in zip(self.process_name_list, self.process_status_list):
                putline.append("[{}] {}".format(name, status))
        
        if self.user_list:
            putline.append("--Users--")
            for user in self.user_list:
                putline.append("[{}] {}".format(user['name'], user['started']))
        
        return "\n".join(putline)

    async def get_check_easy(self, max_performance_percent=[92,92,92]):
        putline = []
        check_list = await self.get_check_simple()

        if sum(check_list) != 0:
            xlogger.error("Computer problem detected. check code: {}".format(check_list))
            if sum(check_list) == 5:
                return "我去世了……（安详"
            if sum(check_list) == 4:
                return "你们如果还能看到消息一定是奇迹……"
            if sum(check_list[:3]) != 0:
                return "啊……我感觉……好热……"
            if sum(check_list[3:5]) == 2:
                return "谁拔我网线?!"
            if check_list[4] == 1:
                return "我节点又断惹(识图、上车等部分功能会受到影响)"
            return "我似乎出了点问题……"

    async def get_check_simple(self, max_performance_percent=[92,92,92]) -> list:
        check_list = [0,0,0,0,0,0]
        self.run_all_check()

        if self.cpu_percent > max_performance_percent[0]:
            check_list[0] = 1
        if self.memory_percent > max_performance_percent[1]:
            check_list[1] = 1
        if self.disk_percent > max_performance_percent[2]:
            check_list[2] = 1
        if self.baidu != 200:
            check_list[3] = 1
        if self.google != 200:
            check_list[4] = 1
        for status in self.process_status_list:
            if status != 'running':
                check_list[5] = 1
                break
        
        return check_list

    def get_performance_check(self):
        self.cpu_percent = psutil.cpu_percent()
        self.memory_percent = psutil.virtual_memory().percent
        self.disk_percent = psutil.disk_usage("/").percent

    def get_network_check(self):
        try:
            self.baidu = requests.get("http://www.baidu.com").status_code
        except:
            self.baidu = 404
            xlogger.warning("Baidu request failed.")

        try:
            self.google = requests.get("http://www.google.com").status_code
        except:
            self.google = 404
            xlogger.warning("Google request failed.")
            
    def get_users_check(self):
        user_list = []
        suser_l = psutil.users()

        for suser in suser_l:
            user = {
                'name': suser.name, 
                'started': datetime.fromtimestamp(suser.started).strftime("%Y-%m-%d %H:%M:%S")}
            user_list.append(user)

        self.user_list = user_list

    def get_process_status(self, request_name_list: set):
        if not request_name_list:
            return None
        
        self.process_name_list = []
        self.process_status_list = []
        
        for p_n in request_name_list:
            p_l = self.get_sname_process_list(p_n)
            if len(p_l) == 1:
                self.process_name_list.append(p_n)
                self.process_status_list.append(p_l[0].status())
            else:
                for i, p in enumerate(p_l):
                    self.process_name_list.append(p_n+" ({})".format(i))
                    self.process_status_list.append(p.status())

    @staticmethod
    def get_sname_process_list(name: str) -> list:
        p_l = []
        pids  = psutil.pids()

        for pid in pids:
            p = psutil.Process(pid)
            if (p.name() == name):
                p_l.append(p)

        return p_l
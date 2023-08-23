from base64 import b64decode, b64encode
import json
import os
import pandas as pd
from prettytable import PrettyTable


# DEBUG = True
SAVESDIR = "D:\Steam\steamapps\common\SlayTheSpire\saves"
DATABASE = "Data\config.json"


def read_file(filename):
    try:
        with open(filename) as file:
            return file.read()
    except FileNotFoundError:
        print(f'文件"{filename}"不存在，请检查文件名或路径')
        exit()
    except IOError:
        print(f'文件"{filename}"打开或读取失败，请检查文件权限或内容')
        exit()


class database(object):
    def __init__(self, filename=DATABASE):
        self.db_json = json.loads(read_file(filename))
        self.db_cards = pd.read_csv(self.db_json["cards"])
        self.db_relics = pd.read_csv(self.db_json["relics"])
        self.energy_relics = self.db_json["energy_relics"]

    def get_job_from_num(self, num: int) -> str:
        return self.db_json["jobs"][num]

    def show_db_cards(self):
        print(self.db_cards)

    def show_db_relics(self):
        print(self.db_relics)

    def get_card_id(self, card_str):
        card_find = self.db_cards[self.db_cards["name"] == card_str]["card_id"].to_list()
        if len(card_find) == 0:
            print(f'卡牌"{card_str}"不存在')
        elif len(card_find) > 1:
            print(f'卡牌"{card_str}"找到{len(card_find)}个结果')
        else:
            return card_find[0]
        exit()

    def get_card_str(self, card_id):
        card_find = self.db_cards[self.db_cards["card_id"] == card_id]["name"].to_list()
        if len(card_find) == 0:
            print(f'卡牌"{card_id}"不存在')
        elif len(card_find) > 1:
            print(f'卡牌"{card_id}"找到{len(card_find)}个结果')
        else:
            return card_find[0]
        exit()

    def get_relic_id(self, relic_str):
        relic_find = self.db_relics[self.db_relics["name_zhs"] == relic_str]["name_en"].to_list()
        if len(relic_find) == 0:
            print(f'遗物"{relic_str}"不存在')
        elif len(relic_find) > 1:
            print(f'遗物"{relic_str}"找到{len(relic_find)}个结果')
        else:
            return relic_find[0]
        exit()

    def get_relic_str(self, relic_id):
        relic_find = self.db_relics[self.db_relics["name_en"] == relic_id]["name_zhs"].to_list()
        if len(relic_find) == 0:
            print(f'遗物"{relic_id}"不存在')
        elif len(relic_find) > 1:
            print(f'遗物"{relic_id}"找到{len(relic_find)}个结果')
        else:
            return relic_find[0]
        exit()

    def is_energy(self, relic_id):
        return relic_id in self.energy_relics


class autosave(object):
    def __init__(self, job=""):
        self.save_state = True
        if job == "":
            self.init_state = False
        else:
            self.init_job(job)

    '''Save'''

    def decode_from_autosave(self, data, key="key"):
        result = ""
        data = b64decode(data)
        for index, data_i in enumerate(data):
            result += chr(data_i ^ ord(key[index % len(key)]))

        result = json.loads(result)
        return result

    def encode_to_autosave(self, data, key="key") -> str:
        result = ""
        data = json.dumps(data).encode()
        for index, data_i in enumerate(data):
            result += chr(data_i ^ ord(key[index % len(key)]))

        result = b64encode(result.encode()).decode()
        return result

    def init_autosave(self, job: str):
        self.init_state = True
        filename = SAVESDIR + "/" + job + ".autosave"
        self.save_json = self.decode_from_autosave(read_file(filename))
        self.job_name = job
        print(f"加载存档成功")
        return

    def write_autosave(self):
        if not self.init_state:
            return
        filename = self.job_name + ".json"
        with open(filename, "w") as wr_json_f:
            wr_json_f.write(json.dumps(self.save_json))
        print(f"存档已写入文件{filename}")
        return

    def save_autosave(self):
        autosave = self.encode_to_autosave(self.save_json)
        filename = SAVESDIR + "/" + self.job_name + ".autosave"
        filename_back = filename + ".back"

        if os.path.exists(filename_back):
            os.remove(filename_back)
        os.rename(filename, filename_back)

        with open(filename, "w") as wr_autosave_f:
            wr_autosave_f.write(autosave)

        self.save_state = True
        print(f'保存存档成功，旧存档备份为".back"后缀')
        return

    def show_autosave(self):
        """
        current_health	目前血量\n
        max_health	最大血量\n
        gold	金币\n
        relics	遗物\n
        cards	当前卡牌，upgrades表示是否升级\n
        hand_size	手牌数量（最大不能大于10如果大于10，还是会按照10来算）\n
        red	能量点\n"""

        global db

        print(f'{"[目前血量]":<10}\t{self.save_json["current_health"]:<5}')
        print(f'{"[最大血量]":<10}\t{self.save_json["max_health"]:<5}')
        print(f'{"[金币]":<10}\t{self.save_json["gold"]:<5}')
        print(f'{"[手牌数量]":<10}\t{self.save_json["hand_size"]:<5}')
        print(f'{"[能量点]":<10}\t{self.save_json["red"]:<5}')

        print(f"[遗物]")
        relic_table = PrettyTable(["name", "id"])
        for relic_id in self.save_json["relics"]:
            relic_table.add_row([db.get_relic_str(relic_id), relic_id])
        print(relic_table)

        print(f"[当前卡牌]")
        card_table = PrettyTable(["name", "id", "upgrades"])
        for card in self.save_json["cards"]:
            card_table.add_row([db.get_card_str(card["id"]), card["id"], card["upgrades"]])
        print(card_table)

        return

    '''Card'''

    def find_card(self, card_id, upgrades) -> int:
        for i, card in enumerate(self.save_json["cards"]):
            if card["id"] == card_id and card["upgrades"] == upgrades:
                return i
        return -1

    def add_card(self, card_str, card_id, upgrades, cnt):
        for i in range(cnt):
            self.save_json["cards"].append({"upgrades": upgrades, "misc": 0, "id": card_id})
        self.save_state = False
        print(f'添加卡牌"name={card_str}, id={card_id}, upgrades={upgrades}"{cnt}张成功')
        return

    def upgrades_card(self, card_str, card_id, upgrades, cnt, need):
        for i in range(cnt):
            index = self.find_card(card_id, upgrades)
            if index == -1:
                print(f'找不到卡牌"name={card_str}, id={card_id}, upgrades={upgrades}"。已经升级了{i}张')
                return
            else:
                self.save_json["cards"][index]["upgrades"] = need
                self.save_state = False
        print(f'升级卡牌"name={card_str}, id={card_id}, upgrades={upgrades}"{cnt}张为{need}级成功')
        return

    def remove_card(self, card_str, card_id, upgrades, cnt):
        for i in range(cnt):
            index = self.find_card(card_id, upgrades)
            if index == -1:
                print(f'找不到卡牌"name={card_str}, id={card_id}, upgrades={upgrades}"。已经删除了{i}张')
                return
            else:
                del self.save_json["cards"][index]
                self.save_state = False
        print(f'删除卡牌"name={card_str}, id={card_id}, upgrades={upgrades}"{cnt}张成功')
        return

    '''Relic'''

    def find_relic(self, relic_id) -> int:
        for i, relic in enumerate(self.save_json["relics"]):
            if relic == relic_id:
                return i
        return -1

    def add_relic(self, relic_str, relic_id):
        global db
        self.save_json["relics"].append(relic_id)
        if db.is_energy(relic_id):
            self.save_json["red"] += 1
        self.save_state = False
        print(f'添加遗物"name={relic_str}, id={relic_id}"成功')
        return

    def remove_relic(self, relic_str, relic_id):
        index = self.find_relic(relic_id)
        if index == -1:
            print(f'找不到遗物"name={relic_str}, id={relic_id}"')
        else:
            del self.save_json["relics"][index]
            self.save_state = False
            print(f'删除遗物"name={relic_str}, id={relic_id}"成功')
        return

    '''Gold'''

    def update_gold(self, gold):
        old = self.save_json["gold"]
        self.save_json["gold"] = gold
        self.save_state = False
        print(f"将金币从{old}更改为{gold}成功")
        return

    '''Health'''

    def update_health(self, health):
        old = self.save_json["current_health"]
        self.save_json["current_health"] = health
        self.save_state = False
        print(f"将血量从{old}更改为{health}成功")
        return


db = database()  # database class save the json from DATABASE
save = autosave()  # autosave class save the job name


def init(dir):
    global SAVESDIR
    SAVESDIR = dir
    return

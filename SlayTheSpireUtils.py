from base64 import b64decode, b64encode
import json
import os
import pandas as pd
from prettytable import PrettyTable


# DEBUG = True
SAVESDIR = "D:\Steam\steamapps\common\SlayTheSpire\saves"
DATABASE = "SlayTheSpireData\config.json"


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

    def get_job_from_num(self, num: int) -> str:
        return self.db_json["jobs"][num]


class autosave(object):
    def __init__(self, job=""):
        self.save_state = True
        if job == "":
            self.init_state = False
        else:
            self.init_job(job)

    def init_job(self, job: str):
        self.init_state = True
        filename = SAVESDIR + "/" + job + ".autosave"
        self.save_json = self.decode_from_autosave(read_file(filename))
        self.job_name = job

    '''Decoding & Encoding'''

    def decode_from_autosave(self, data, key="key"):
        result = ""
        data = b64decode(data)
        for index, data_i in enumerate(data):
            result += chr(data_i ^ ord(key[index % len(key)]))

        result = json.loads(result)
        return result

    def encode_to_autosave(self, data, key="key"):
        result = ""
        data = json.dumps(data).encode()
        for index, data_i in enumerate(data):
            result += chr(data_i ^ ord(key[index % len(key)]))

        result = b64encode(result.encode()).decode()
        return result

    def write_to_json_file(self):
        if not self.init_state:
            return
        with open(self.job_name + ".json", "w") as wr_json_f:
            wr_json_f.write(json.dumps(self.save_json))

    '''Card'''

    def add_card_to_json(self, id, upgrades):
        self.save_state = False
        self.save_json["cards"].append({"upgrades": upgrades, "misc": 0, "id": id})
        return

    def find_card_by_id_and_upgrades(self, id, upgrades):
        for i, card in enumerate(self.save_json["cards"]):
            if card["id"] == id and card["upgrades"] == upgrades:
                return i
        print(f'找不到卡牌"id={id}, upgrades={upgrades}"')
        exit()

    def upgrades_card_to_json(self, id, upgrades):
        index = self.find_card_by_id_and_upgrades(id, upgrades)
        self.save_state = False
        self.save_json["cards"][index]["upgrades"] += 1
        return

    def remove_card_to_json(self, id, upgrades):
        index = self.find_card_by_id_and_upgrades(id, upgrades)
        self.save_state = False
        del self.save_json["cards"][index]
        return

    '''Relic'''

    def add_relic_to_json(self, id):
        self.save_state = False
        self.save_json["relics"].append(id)
        return

    def find_relic_by_id(self, id):
        for i, relic in enumerate(self.save_json["relics"]):
            if relic == id:
                return i
        print(f'找不到遗物"id={id}"')
        exit()

    def remove_relic_to_json(self, id):
        index = self.find_relic_by_id(id)
        self.save_state = False
        del self.save_json["relics"][index]
        return

    '''Gold'''

    def update_gold_to_json(self, gold):
        self.save_state = False
        old = self.save_json["gold"]
        self.save_json["gold"] = gold
        return old

    '''Save'''

    def save_to_autosave(self):
        self.save_state = True
        autosave = self.encode_to_autosave(self.save_json)

        filename = SAVESDIR + "/" + self.job_name + ".autosave"
        filename_back = filename + ".back"
        if os.path.exists(filename_back):
            os.remove(filename_back)
        os.rename(filename, filename_back)

        with open(filename, "w") as wr_autosave_f:
            wr_autosave_f.write(autosave)
        return

    def show(self):
        """
        current_health	目前血量\n
        max_health	最大血量\n
        gold	金币\n
        relics	遗物\n
        cards	当前卡牌，upgrades表示是否升级\n
        hand_size	手牌数量（最大不能大于10如果大于10，还是会按照10来算）\n
        red	能量点\n"""
        print(f'{"[目前血量]":<10}\t{self.save_json["current_health"]:<5}')
        print(f'{"[最大血量]":<10}\t{self.save_json["max_health"]:<5}')
        print(f'{"[金币]":<10}\t{self.save_json["gold"]:<5}')
        print(f'{"[手牌数量]":<10}\t{self.save_json["hand_size"]:<5}')
        print(f'{"[能量点]":<10}\t{self.save_json["red"]:<5}')
        print(f"[遗物]")
        relic_table = PrettyTable(["name", "id"])
        for relic_id in self.save_json["relics"]:
            relic_table.add_row([get_relic_str(relic_id), relic_id])
        print(relic_table)
        print(f"[当前卡牌]")
        card_table = PrettyTable(["name", "id", "upgrades"])
        for card in self.save_json["cards"]:
            card_table.add_row([get_card_str(card["id"]), card["id"], card["upgrades"]])
        print(card_table)
        return


db = database()  # database class save the json from DATABASE
save = autosave()  # autosave class save the job name

"""DATABASE FUNCTIONS"""


def show_db_cards():
    global db
    print(db.db_cards)


def show_db_relics():
    global db
    print(db.db_relics)


def get_card_id(card_str):
    global db
    card_find = db.db_cards[db.db_cards["name"] == card_str]["card_id"].to_list()
    if len(card_find) == 0:
        print(f'卡牌"{card_str}"不存在')
    elif len(card_find) > 1:
        print(f'卡牌"{card_str}"找到{len(card_find)}个结果')
    else:
        return card_find[0]
    exit()


def get_card_str(card_id):
    global db
    card_find = db.db_cards[db.db_cards["card_id"] == card_id]["name"].to_list()
    if len(card_find) == 0:
        print(f'卡牌"{card_id}"不存在')
    elif len(card_find) > 1:
        print(f'卡牌"{card_id}"找到{len(card_find)}个结果')
    else:
        return card_find[0]
    exit()


def get_relic_id(relic_str):
    global db
    relic_find = db.db_relics[db.db_relics["name_zhs"] == relic_str]["name_en"].to_list()
    if len(relic_find) == 0:
        print(f'遗物"{relic_str}"不存在')
    elif len(relic_find) > 1:
        print(f'遗物"{relic_str}"找到{len(relic_find)}个结果')
    else:
        return relic_find[0]
    exit()


def get_relic_str(relic_id):
    global db
    relic_find = db.db_relics[db.db_relics["name_en"] == relic_id]["name_zhs"].to_list()
    if len(relic_find) == 0:
        print(f'遗物"{relic_id}"不存在')
    elif len(relic_find) > 1:
        print(f'遗物"{relic_id}"找到{len(relic_find)}个结果')
    else:
        return relic_find[0]
    exit()


"""SAVE FUNCTIONS"""


def job_choose(job: int):
    """
    Args:
        job: int between 1 to 4
    """
    global save
    save.init_job(db.get_job_from_num(job - 1))
    print(f"加载存档成功")


def show_save():
    global save
    save.show()
    return


def write_json():
    global save
    save.write_to_json_file()
    return


def add_card(card_id, upgrades):
    global save
    save.add_card_to_json(card_id, upgrades)
    print(f'添加卡牌"id={card_id}, upgrades={upgrades}"成功')
    return


def upgrades_card(card_id, upgrades):
    global save
    save.upgrades_card_to_json(card_id, upgrades)
    print(f'升级卡牌"id={card_id}, upgrades={upgrades}"成功')
    return


def remove_card(card_id, upgrades):
    global save
    save.remove_card_to_json(card_id, upgrades)
    print(f'删除卡牌"id={card_id}, upgrades={upgrades}"成功')
    return


def add_relic(relic_id):
    global save
    save.add_relic_to_json(relic_id)
    print(f'添加遗物"id={relic_id},"成功')
    return


def remove_relic(relic_id):
    global save
    save.remove_relic_to_json(relic_id)
    print(f'删除遗物"id={relic_id},"成功')
    return


def update_gold(gold):
    global save
    old = save.update_gold_to_json(gold)
    print(f"将金币从{old}更改为{gold}成功")
    return


def save_save():
    global save
    save.save_to_autosave()
    print(f'保存存档成功，旧存档备份为".back"后缀')
    return


def init(dir):
    global SAVESDIR
    SAVESDIR = dir
    return

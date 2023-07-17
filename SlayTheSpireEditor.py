# import json
import os
import SlayTheSpireUtils as utils


def clear():
    os.system("cls")


def input_options(option_list):
    prompt = "========================\n请选择:\n"
    for i, option in enumerate(option_list, 1):
        prompt += f"{i}. {option}\n"
    prompt += "其他输入退出"
    return prompt


def show_db():
    options = ["查看卡牌", "查看遗物"]
    while True:
        clear()
        choice = input(input_options(options))
        if choice == "1":
            utils.db.show_db_cards()
        elif choice == "2":
            utils.db.show_db_relics()
        else:
            break


def edit_save():
    clear()
    # choose job
    options = ["铁甲战士", "静默猎手", "故障机器人", "观者"]
    choice = input(input_options(options))
    match choice:
        case "1" | "2" | "3" | "4":
            utils.save.init_autosave(utils.db.get_job_from_num(int(choice) - 1))
            # utils.job_choose(int(choice))
        case _:
            return
    # choose func
    options = {
        "展示存档状态": utils.save.show_autosave,
        "解码存档到json": utils.save.write_autosave,
        "添加卡牌": lambda: utils.save.add_card(*card_to_id()),
        "升级卡牌": lambda: utils.save.upgrades_card(*card_to_id()),
        "删除卡牌": lambda: utils.save.remove_card(*card_to_id()),
        "添加遗物": lambda: utils.save.add_relic(*relic_to_id()),
        "删除遗物": lambda: utils.save.remove_relic(*relic_to_id()),
        "修改金币": update_gold,
        "保存修改": utils.save.save_autosave,
    }
    while True:
        choice = input(input_options(options))
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            clear()
            list(options.values())[int(choice) - 1]()
        else:
            break
    if not utils.save.save_state:
        choice = input("存档尚未保存，输入回车保存更改，其他输入取消更改")
        if choice == "":
            utils.save.save_autosave()


def card_to_id():
    card = input("========================\n请输入卡牌中文名称:")
    upgrades_str = input("请输入卡牌等级，默认及任何非法输入视为0:")
    upgrades = 0
    if upgrades_str.isdigit():
        upgrades = int(upgrades_str)
    return card, utils.db.get_card_id(card), upgrades


def relic_to_id():
    relic = input("========================\n请输入遗物中文名称:")
    return relic, utils.db.get_relic_id(relic)


def update_gold():
    gold = input("========================\n请输入金币数:")
    if gold.isdigit():
        utils.save.update_gold(int(gold))
    else:
        print(f"{gold}不是合法数字")


def main_loop_all():
    options = ["查看数据库", "修改存档"]
    while True:
        clear()
        choice = input(input_options(options))
        if choice == "1":
            show_db()
        elif choice == "2":
            edit_save()
        else:
            break


def main_loop():
    # main_loop_all()
    edit_save()


if __name__ == "__main__":
    saves_dir = "D:\Steam\steamapps\common\SlayTheSpire\saves"
    utils.init(saves_dir)

    main_loop()

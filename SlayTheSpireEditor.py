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
            utils.show_db_cards()
        elif choice == "2":
            utils.show_db_relics()
        else:
            break


def edit_save():
    clear()
    # choose job
    options = ["铁甲战士", "静默猎手", "故障机器人", "观者"]
    choice = input(input_options(options))
    match choice:
        case "1" | "2" | "3" | "4":
            utils.job_choose(int(choice))
        case _:
            return
    # choose func
    options = ["展示存档状态", "解码存档到json", "添加卡牌", "升级卡牌", "删除卡牌", "修改金币", "保存修改"]
    while True:
        choice = input(input_options(options))
        match choice:
            case "1":
                clear()
                utils.show_save()
            case "2":
                utils.write_json()
            case "3":
                card_id, upgrades = card_to_id()
                utils.add_card(card_id, upgrades)
            case "4":
                card_id, upgrades = card_to_id()
                utils.upgrades_card(card_id, upgrades)
            case "5":
                card_id, upgrades = card_to_id()
                utils.remove_card(card_id, upgrades)
            case "6":
                update_gold()
            case "7":
                utils.save_save()
            case _:
                break
        input("任意输入继续")
    if not utils.save.save_state:
        choice = input("存档尚未保存，输入回车保存更改，其他输入取消更改")
        if choice == "":
            utils.save_save()


def card_to_id():
    clear()
    card = input("========================\n请输入卡牌中文名称:")
    upgrades_str = input("请输入卡牌等级，默认及任何非法输入视为0:")
    upgrades = 0
    if upgrades_str.isdigit():
        upgrades = int(upgrades_str)
    return utils.get_card_id(card), upgrades


def update_gold():
    clear()
    gold = input("========================\n请输入金币数:")
    if gold.isdigit():
        utils.update_gold(int(gold))
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

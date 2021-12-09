import random
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD
from vkbottle import GroupEventType, GroupTypes, VKAPIError
from vkbottle import BaseStateGroup
from vkbottle import CtxStorage
from time import sleep

bot = Bot(token='5321a29b3d62cd089589a1d712ba66db267de73b53efc5d1be3b2c4e7983811394e9687caf89f5d49352c')
ctx = CtxStorage()
bot.labeler.vbml_ignore_case = True

class EditFile(BaseStateGroup):
        NONE_FILE = 0
        GACHI_FILE_EDIT_NUM = 1
        GACHI_FILE_EDIT_STR = 2
        GACHI_FILE_ADD = 3
        PRICE_FILE_EDIT_NUM = 4
        PRICE_FILE_EDIT_STR = 5
        PRICE_FILE_ADD = 6
        VKUS_FILE_EDIT_NUM = 7
        VKUS_FILE_EDIT_STR = 8
        VKUS_FILE_ADD = 9
        VIDEO_FILE_EDIT_NUM = 10
        VIDEO_FILE_EDIT_STR = 11
        VIDEO_FILE_ADD = 12

msg_start = ["начать", "привет", "старт"]
msg_vkus = ["вкусы", "вкус"]
msg_price = ["цены", "цена", "стоимость"]
msg_order = ["заказать", "заказ"]
msg_gachi = ["гачи", "гачи анекдот", "анекдот"]
msg_bad = ["долбаёб", "пиздюк", "долбаеб", "долбоёб", "долбоеб"]
msg_nah = ["пошёл нахуй", "нахуй", "пошел нахуй", "пошёл на хуй", "иди нахуй", "иди на хуй"]
msg_good = ["хорошо", "спасибо", "хаха"]
msg_by = ["пока", "выход"]

#=============================================================================================================================================================================================================================================================
#Меню разработчика
#=============================================================================================================================================================================================================================================================

@bot.on.message(payload={"dev": "menu"})
@bot.on.message(text="Dev")
async def menu_dev(message: Message):
        if message.from_id == 253309814:
                keyboard = Keyboard()

                keyboard.add(Text("gachi.txt", {"dev": "gachi"}))
                keyboard.row()
                keyboard.add(Text("price.txt", {"dev": "price"}))
                keyboard.row()
                keyboard.add(Text("vkus.txt", {"dev": "vkus"}))
                keyboard.row()
                keyboard.add(Text("video.txt", {"dev": "video"}))
                keyboard.row()
                keyboard.add(Text("Exit", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)

                await message.answer("Меню разработчика: \ngachi.txt \nprice.txt \nvkus.txt \nExit", keyboard = keyboard)
        else:
                await message.answer(f"Ты не мой папа! {message.from_id}")

@bot.on.message(payload={"dev": "gachi"})
async def gachi_dev(message: Message):
        keyboard = Keyboard()

        keyboard.add(Text("Показать", {"dev": "view_gachi"}))
        keyboard.add(Text("Исправить", {"dev": "edit_gachi"}))
        keyboard.add(Text("Добавить", {"dev": "add_gachi"}))
        keyboard.row()
        keyboard.add(Text("Назад", {"dev": "menu"}), color=KeyboardButtonColor.NEGATIVE)

        await message.answer("Выберите режим", keyboard=keyboard)

@bot.on.message(payload={"dev": "price"})
async def price_dev(message: Message):
        keyboard = Keyboard()

        keyboard.add(Text("Показать", {"dev": "view_price"}))
        keyboard.add(Text("Исправить", {"dev": "edit_price"}))
        keyboard.add(Text("Добавить", {"dev": "add_price"}))
        keyboard.row()
        keyboard.add(Text("Назад", {"dev": "menu"}), color=KeyboardButtonColor.NEGATIVE)

        await message.answer("Выберите режим", keyboard=keyboard)

@bot.on.message(payload={"dev": "vkus"})
async def vkus_dev(message: Message):
        keyboard = Keyboard()

        keyboard.add(Text("Показать", {"dev": "view_vkus"}))
        keyboard.add(Text("Исправить", {"dev": "edit_vkus"}))
        keyboard.add(Text("Добавить", {"dev": "add_vkus"}))
        keyboard.row()
        keyboard.add(Text("Назад", {"dev": "menu"}), color=KeyboardButtonColor.NEGATIVE)

        await message.answer("Выберите режим", keyboard=keyboard)

@bot.on.message(payload={"dev": "video"})
async def video_dev(message:Message):
    keyboard = Keyboard()

    keyboard.add(Text("Показать", {"dev": "view_video"}))
    keyboard.add(Text("Исправить", {"dev": "edit_video"}))
    keyboard.add(Text("Добавить", {"dev": "add_video"}))
    keyboard.row()
    keyboard.add(Text("Назад", {"dev": "menu"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer("Выберите режим", keyboard=keyboard)

#=========================Edit for gachi.txt===============================================
@bot.on.message(payload={"dev": "view_gachi"})
async def gachi_dev_view(message: Message):
        with open('gachi.txt', 'r', encoding='utf-8') as f:
                g = f.readlines()
                await message.answer('\n'.join(g))
        message.payload = {"dev": "gachi"}

@bot.on.message(payload={"dev": "edit_gachi"})
async def gachi_dev_edit(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.GACHI_FILE_EDIT_NUM)
        return "Введите НОМЕР СТРОКИ для замены"

@bot.on.message(state=EditFile.GACHI_FILE_EDIT_NUM)
async def gachi_dev_edit_number(message: Message):
        ctx.set("gachi_num", message.text)
        await bot.state_dispenser.set(message.peer_id, EditFile.GACHI_FILE_EDIT_STR)
        return "Введите новую строку"

@bot.on.message(state=EditFile.GACHI_FILE_EDIT_STR)
async def gachi_dev_edit_str(message: Message):
        num = int(ctx.get("gachi_num"))
        new_str = message.text
        license_edit = []
        with open('gachi.txt', 'r', encoding='utf-8') as f:
                license_edit = f.readlines()
        license_edit.remove(license_edit[num])
        license_edit.insert(num, new_str+'\n')
        f = open('gachi.txt', 'w')
        f.close()
        with open('gachi.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(license_edit))
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "gachi"}
        return "Успех"

@bot.on.message(payload={"dev": "add_gachi"})
async def gachi_dev_add(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.GACHI_FILE_ADD)
        return "Введите строку, которую надо добавить"

@bot.on.message(state=EditFile.GACHI_FILE_ADD)
async def gachi_dev_add_str(message: Message):
        new_str = message.text
        with open('gachi.txt', 'a', encoding='utf-8') as f:
                f.write('\n'+new_str)
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "gachi"}
        return "Успех"

#=========================Edit for price.txt===============================================
@bot.on.message(payload={"dev": "view_price"})
async def price_dev_view(message: Message):
        with open('price.txt', 'r', encoding='utf-8') as f:
                g = f.readlines()
                await message.answer(''.join(g))
        message.payload = {"dev": "price"}

@bot.on.message(payload={"dev": "edit_price"})
async def price_dev_edit(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.PRICE_FILE_EDIT_NUM)
        return "Введите НОМЕР СТРОКИ для замены"

@bot.on.message(state=EditFile.PRICE_FILE_EDIT_NUM)
async def price_dev_edit_number(message: Message):
        ctx.set("price_num", message.text)
        await bot.state_dispenser.set(message.peer_id, EditFile.PRICE_FILE_EDIT_STR)
        return "Введите новую строку"

@bot.on.message(state=EditFile.PRICE_FILE_EDIT_STR)
async def price_dev_edit_str(message: Message):
        num = int(ctx.get("price_num"))
        new_str = message.text
        license_edit = []
        with open('price.txt', 'r', encoding='utf-8') as f:
                license_edit = f.readlines()
        license_edit.remove(license_edit[num])
        license_edit.insert(num, new_str+'\n')
        f = open('price.txt', 'w')
        f.close()
        with open('price.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(license_edit))
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "price"}
        return "Успех"

@bot.on.message(payload={"dev": "add_price"})
async def price_dev_add(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.PRICE_FILE_ADD)
        return "Введите строку, которую надо добавить"

@bot.on.message(state=EditFile.PRICE_FILE_ADD)
async def price_dev_add_str(message: Message):
        new_str = message.text
        with open('price.txt', 'a', encoding='utf-8') as f:
                f.write('\n'+new_str)
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "price"}
        return "Успех"

#=========================Edit for vkus.txt===============================================
@bot.on.message(payload={"dev": "view_vkus"})
async def vkus_dev_view(message: Message):
        with open('vkus.txt', 'r', encoding='utf-8') as f:
                g = f.readlines()
                await message.answer(''.join(g))
        message.payload = {"dev": "vkus"}

@bot.on.message(payload={"dev": "edit_vkus"})
async def vkus_dev_edit(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.VKUS_FILE_EDIT_NUM)
        return "Введите НОМЕР СТРОКИ для замены"

@bot.on.message(state=EditFile.VKUS_FILE_EDIT_NUM)
async def vkus_dev_edit_number(message: Message):
        ctx.set("vkus_num", message.text)
        await bot.state_dispenser.set(message.peer_id, EditFile.VKUS_FILE_EDIT_STR)
        return "Введите новую строку"

@bot.on.message(state=EditFile.VKUS_FILE_EDIT_STR)
async def vkus_dev_edit_str(message: Message):
        num = int(ctx.get("vkus_num"))
        new_str = message.text
        license_edit = []
        with open('vkus.txt', 'r', encoding='utf-8') as f:
                license_edit = f.readlines()
        license_edit.remove(license_edit[num])
        license_edit.insert(num, new_str+'\n')
        f = open('vkus.txt', 'w')
        f.close()
        with open('vkus.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(license_edit))
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "vkus"}
        return "Успех"

@bot.on.message(payload={"dev": "add_vkus"})
async def vkus_dev_add(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.VKUS_FILE_ADD)
        return "Введите строку, которую надо добавить"

@bot.on.message(state=EditFile.VKUS_FILE_ADD)
async def vkus_dev_add_str(message: Message):
        new_str = message.text
        with open('vkus.txt', 'a', encoding='utf-8') as f:
                f.write('\n'+new_str)
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "vkus"}
        return "Успех"

#=========================Edit for video.txt===============================================
@bot.on.message(payload={"dev": "view_video"})
async def video_dev_view(message: Message):
        with open('video.txt', 'r', encoding='utf-8') as f:
                g = f.readlines()
                await message.answer('\n'.join(g))
        message.payload = {"dev": "video"}

@bot.on.message(payload={"dev": "edit_video"})
async def video_dev_edit(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.VIDEO_FILE_EDIT_NUM)
        return "Введите НОМЕР СТРОКИ для замены"

@bot.on.message(state=EditFile.VIDEO_FILE_EDIT_NUM)
async def video_dev_edit_number(message: Message):
        ctx.set("video_num", message.text)
        await bot.state_dispenser.set(message.peer_id, EditFile.VIDEO_FILE_EDIT_STR)
        return "Введите новую строку"

@bot.on.message(state=EditFile.VIDEO_FILE_EDIT_STR)
async def video_dev_edit_str(message: Message):
        num = int(ctx.get("video_num"))
        new_str = message.text
        license_edit = []
        with open('video.txt', 'r', encoding='utf-8') as f:
                license_edit = f.readlines()
        license_edit.remove(license_edit[num])
        license_edit.insert(num, new_str+'\n')
        f = open('video.txt', 'w')
        f.close()
        with open('video.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(license_edit))
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "video"}
        return "Успех"

@bot.on.message(payload={"dev": "add_video"})
async def video_dev_add(message: Message):
        await bot.state_dispenser.set(message.peer_id, EditFile.VIDEO_FILE_ADD)
        return "Введите строку, которую надо добавить"

@bot.on.message(state=EditFile.VIDEO_FILE_ADD)
async def video_dev_add_str(message: Message):
        new_str = message.text
        with open('video.txt', 'a', encoding='utf-8') as f:
                f.write('\n'+new_str)
        await bot.state_dispenser.set(message.peer_id, EditFile.NONE_FILE)
        message.payload = {"dev": "video"}
        return "Успех"

#=============================================================================================================================================================================================================================================================
#Главное меню
#=============================================================================================================================================================================================================================================================

@bot.on.message(text = msg_start)
async def message_hi(message: Message):
        keyboard = Keyboard()

        user = await bot.api.users.get(message.from_id)
        await message.answer(f"Привет, {user[0].first_name} &#128522;")
        sleep(1)
        await message.answer("Меня зовут Zaёbik")
        sleep(1)
        await message.answer("Я ещё совсем маленький, в отличии от тебя, раз ты решился тут покупать, я знаю мало комманд и совсем немного чего умею, мой папа долбаёб не научил меня ничему")
        sleep(1)

        keyboard.add(Text("Вкусы", {"cmd": "vkus"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Цены", {"cmd": "price"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Заказать"), color=KeyboardButtonColor.POSITIVE)
        keyboard.row()
        keyboard.add(Text("Гачи анекдот", {"cmd": "gachi"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Видосик", {"cmd": "video"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Выход", {"cmd": "exit"}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.row()
        keyboard.add(OpenLink("https://www.instagram.com/zbspuff_msk/", "Инстаграмм"), color=KeyboardButtonColor.POSITIVE)

        await message.answer("Вот несколько комманд, которые я знаю: \n- Вкусы \n- Цены \n- Заказать/заказ \n- Гачи анекдот/гачи/анекдот", keyboard=keyboard)



@bot.on.message(payload = {"cmd": "menu"})
async def message_menu(message: Message):
        keyboard = Keyboard()

        keyboard.add(Text("Вкусы", {"cmd": "vkus"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Цены", {"cmd": "price"}), color=KeyboardButtonColor.POSITIVE)
        keyboard.add(Text("Заказать"), color=KeyboardButtonColor.POSITIVE)
        keyboard.row()
        keyboard.add(Text("Гачи анекдот", {"cmd": "gachi"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Видосик", {"cmd": "video"}), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text("Выход", {"cmd": "exit"}), color=KeyboardButtonColor.NEGATIVE)
        keyboard.row()
        keyboard.add(OpenLink("https://www.instagram.com/zbspuff_msk/", "Инстаграмм"), color=KeyboardButtonColor.POSITIVE)

        await message.answer("Доступные команды: \n- Вкусы \n- Цены \n- Заказать/заказ \n- Гачи анекдот/гачи/анекдот", keyboard=keyboard)

@bot.on.message(text = msg_vkus)
@bot.on.message(payload = {"cmd": "vkus"})
async def message_vkus(message: Message):
        keyboard = Keyboard(one_time = True)

        keyboard.add(Text("Назад", {"cmd": "menu"}), color = KeyboardButtonColor.NEGATIVE)
        with open('vkus.txt', 'r', encoding='utf-8') as f:
                await message.answer("Доступные вкусы:\n"+''.join(f.readlines()), keyboard = keyboard)

@bot.on.message(text = msg_price)
@bot.on.message(payload = {"cmd": "price"})
async def message_price(message: Message):
        keyboard = Keyboard(one_time = True)

        keyboard.add(Text("Назад", {"cmd": "menu"}), color = KeyboardButtonColor.NEGATIVE)
        with open('price.txt', 'r', encoding='utf-8') as f:
                await message.answer(''.join(f.readlines()), keyboard = keyboard)

@bot.on.message(text = msg_order)
async def message_order(message: Message):
        await message.answer("Для заказа писать \nvk:https://vk.com/id645833755")

@bot.on.message(text = msg_gachi)
@bot.on.message(payload = {"cmd": "gachi"})
async def message_gachi(message: Message):
        keyboard = Keyboard(one_time = True)

        keyboard.add(Text("Ещё", {"cmd": "gachi"}), color = KeyboardButtonColor.PRIMARY)
        keyboard.add(Text("Назад", {"cmd": "menu"}), color = KeyboardButtonColor.NEGATIVE)
        with open('gachi.txt', 'r', encoding='utf-8') as f:
                gachi = f.readlines()
                await message.answer(gachi[random.randint(0, (len(gachi) - 1))], keyboard = keyboard)

@bot.on.message(payload = {"cmd": "video"})
async def message_vid(message: Message):
    keyboard = Keyboard(one_time = True)

    keyboard.add(Text("Ещё", {"cmd": "video"}), color = KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Назад", {"cmd": "menu"}), color = KeyboardButtonColor.NEGATIVE)
    with open('video.txt', 'r', encoding='utf-8') as f:
        video_smeh = f.readlines()
        await message.answer("", keyboard = keyboard, attachment = video_smeh[random.randint(0, (len(video_smeh) - 1))])

@bot.on.message(text = msg_bad)
async def message_bad(message: Message):
        await message.answer(attachment="video-209400635_456239049")

@bot.on.message(text=["чёрт", "черт", "чертила"])
async def message_1(message: Message):
        await message.answer(attachment="video-209400635_456239028")

@bot.on.message(text=['я твою мать ебал', 'мать ебал', 'мамку твою ебал', 'мать твою ебал', 'я твоего папу ебал', 'отца ебал', 'отца твоего ебал', 'батю твоего ебал', 'батю ебал'])
async def message_2(message: Message):
        await message.answer(attachment="video-209400635_456239035")

@bot.on.message(text=["пидр", 'пидарас', 'хуй', 'хуесос', "хуйло"])
async def message_3(message: Message):
        await message.answer(attachment="video-209400635_456239066")

@bot.on.message(text=['соси', 'саси', 'отсоси', 'отсаси'])
async def message_4(message: Message):
        await message.answer(attachment="video-209400635_456239065")

@bot.on.message(text=["покемон", "старый"])
async def message_5(message: Message):
        await message.answer(attachment="video-209400635_456239041")

@bot.on.message(text=['Анастасися', 'Дарина5', 'Полено'])
async def message_6(message: Message):
        await message.answer("Лучшая! Слегка ебанутая")

@bot.on.message(text=msg_nah)
async def message_nah(message: Message):
    await message.answer(attachment="video-209400635_456239017")

@bot.on.message(text = msg_good)
async def message_good(message: Message):
        await message.answer("&#128522;")

@bot.on.message(text = msg_by)
@bot.on.message(payload = {"cmd": "exit"})
async def message_by(message: Message):
        await message.answer("Пока, надеюсь я тебе помог или развлёк)", keyboard = EMPTY_KEYBOARD)

bot.run_forever()

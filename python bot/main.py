from pytube import YouTube #Импортируем билбиотеку для скачивания видео с ютуб
import os #Это библиотека будет нужна для создания папки для видео каждого пользователя
import validators #Проверка валидности ссылки
from config import TOKEN #Импортируем наш токен бота из файла config

from aiogram import Bot, Dispatcher, executor, types #Основная библиотека aiogram, на ней будет написан сам бот
import shutil

#Создаем диспетчера, который будет управлять ботом
bot = Bot(TOKEN)
dp = Dispatcher(bot)




#Этот декоратор нужен для первого запуска бота и обработки команды старт
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    name = message.from_user.first_name #сохраняем себе ник пользователя
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEEEAtiI7Ce0etpeOHt8NxU6WYAAeuU6DYAAgUAA8A2TxP5al-agmtNdSME")
    #Выше мы отправили пользователю стикер через id
    await message.answer(f"Приветствую, {name}.\nОтправь мне ссылку на ютуб видео!")
    #Ну а тут приветственное сообщение по нику

#Принимаем от пользователя сообщения
@dp.message_handler(content_types=['text'])
async def downloadYouTube(message: types.Message):
    print(message.text) #консольный вывод ссылки или же любого текста сообщения
    try:
        #Проверка валидности ссылки
        if validators.url(message.text):
            yt = YouTube(message.text)
            yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not os.path.exists("./video/"+str(message.from_user.id)):
                os.makedirs("./video/"+str(message.from_user.id))
                #создание папки с id пользователя, если она отсутствует. А она должна отсутвововать.
            await message.answer('Пожалуйста, ожидайте загрузку видео 🙏')
            print('start download') #консольное оповещение
            yt.download("./video/"+str(message.from_user.id), filename=str(message.from_user.id))
            #Первый аргумент это путь к папке пользователя, второй это название видео в виде id
            try:
                print('finish download video and start sending video') #консольное оповещение
                with open('./video/' + str(message.from_user.id) + '/' + str(message.from_user.id), 'rb') as video:
                    await message.answer_video(video) #Открываем папку пользователя и отправляем ему видео
                print('finish sending video') #Консольное оповещение
                shutil.rmtree('./video/' + str(message.from_user.id)) #Удаляем папку пользователя
                await message.answer('Спасибо за использование нашего бота, вы можете снова отправить мне ссылку 🥳')
                #Все получилось. Дальше только обработчики ошибок и уведомление о том, что пользователь отправил не ссылку(вспоминаем нашу библиотеку для проверки ссылок)
            except:
                await message.answer('Не смогли доставить вам видео ☹')
        else:
            await message.answer('Кажется это не ссылка на видео 🤢')
    except:
        await message.answer('К сожелению нам не удалось скачать видео ☹\nПовторите попытку 🥺')





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
import logging
import time
from threading import Thread

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, InlineQueryHandler

from youtube_money_maker.youtube_money_maker import youtube_money_maker

# queue = []
# ymm = youtube_money_maker()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def new_music_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arguments = update.message.text.split(" ")

    image_url = arguments[1]
    audio_url = arguments[2]

    ymm = youtube_money_maker()

    image_downloaded = ymm.downloadImage(url=image_url)
    music_downloaded = ymm.downloadMusic(url=audio_url)

    if image_downloaded and music_downloaded:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Download successful.")
        music_video_generated, file_name = ymm.add_static_image_to_audio()
        if music_video_generated:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Musicvideo is generated.")
            await context.bot.send_video(chat_id=update.effective_chat.id,filename=file_name,video=open(file_name, 'rb'))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occured while generating.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="URLs are probably not correct.")
    # queue.append((update.effective_chat.id,image_url,audio_url))
    # generate_polling()



# def generate_polling():
#     while len(queue) != 0:
#
#
#         job = queue.pop(0)
#         ymm.downloadImage(job[1])
#         ymm.downloadMusic(job[2])
#
#         print(f"JOB DELETED -> {job}")


if __name__ == '__main__':
    application = ApplicationBuilder().token("5437920544:AAHLdpsT0-rqncINFnxwAwRWgtytQCgoGPo").build()
    job_queue = application.job_queue

    # create Handlers
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    new_music_video_handler = CommandHandler('new_music', new_music_video)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # add Handlers
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(new_music_video_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

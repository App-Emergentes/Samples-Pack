from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

import config

app = Client("bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Ya me uní al canal", callback_data="verify_channel")]
    ])
    await message.reply(
        "👋 ¡Hola! Para usar este bot, primero únete a nuestro canal:

"
        f"👉 {config.CANAL_URL}",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("verify_channel"))
async def verify(client, callback_query):
    user = callback_query.from_user
    try:
        member = await client.get_chat_member(config.CANAL_USERNAME, user.id)
        if member.status in ("member", "administrator", "creator"):
            await callback_query.message.edit("✅ Verificado. Bienvenido al menú principal:")
            await show_main_menu(callback_query.message)
        else:
            await callback_query.message.edit("❌ No estás en el canal. Únete y vuelve a intentarlo.")
    except:
        await callback_query.message.edit("⚠️ Error al verificar. Intenta de nuevo.")

async def show_main_menu(message):
    menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Crear Publicación", callback_data="crear_pub"),
         InlineKeyboardButton("📝 Renombrar Archivos", callback_data="renombrar")],
        [InlineKeyboardButton("⏰ Programar", callback_data="programar"),
         InlineKeyboardButton("✏️ Editar", callback_data="editar")],
        [InlineKeyboardButton("📊 Estadísticas", callback_data="estadisticas"),
         InlineKeyboardButton("⚙️ Configuraciones", callback_data="config")]
    ])
    await message.reply("Selecciona una opción del menú:", reply_markup=menu)

app.run()
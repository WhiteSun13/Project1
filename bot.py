import os
import telebot
import paho.mqtt.client as mqtt

# Забираем секреты из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOPIC = os.getenv("MQTT_TOPIC")

# Защита от случайного запуска без настроенных переменных
if not BOT_TOKEN or not TOPIC:
    raise ValueError("❌ Ошибка: В переменных окружения не задан BOT_TOKEN или MQTT_TOPIC!")

bot = telebot.TeleBot(BOT_TOKEN)

# Настройки брокера оставляем в коде, так как это публичные данные
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883

@bot.message_handler(commands=['wake'])
def wake_laptop(message):
    try:
        # Подключаемся к MQTT и отправляем сигнал
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(TOPIC, "WAKE")
        client.disconnect()
        
        bot.reply_to(message, "✅ Сигнал на Raspberry Pi отправлен! Ноутбук просыпается...")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка отправки: {e}")

bot.polling(none_stop=True)
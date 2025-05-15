import requests
import asyncio
from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Application, ContextTypes
from telegram.ext import ConversationHandler, filters
from translate import Translator
import datetime
from config import BOT_TOKEN, api_key_weather, api_key_zones
import sys
import pytz
import logging
import schedule
import time
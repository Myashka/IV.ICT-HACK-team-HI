import datetime
import json
import os
import subprocess
import uuid

import requests
import speech_recognition as sr
import telebot
from telebot import types

import generationText_API
import model
import voiceToSpeech_API as voice_text

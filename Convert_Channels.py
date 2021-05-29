# -*- coding: utf-8 -*-
"""
Created on Fri May 28 20:06:22 2021

@author: ZiphozinhleLuvuno
"""

from pydub import AudioSegment
sound = AudioSegment.from_wav("host1.wav")
sound = sound.set_channels(1)
sound.export("host2.wav", format="wav")

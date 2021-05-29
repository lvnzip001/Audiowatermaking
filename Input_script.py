# -*- coding: utf-8 -*-
"""
Created on Sat May 29 00:29:52 2021

@author: ZiphozinhleLuvuno
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 25 22:09:10 2021

@author: Ziphozihle Luvuno
Reference: Akira Tamamori
"""


""" INPUT SECTION """
import watermark_spread_spectrum as wm
#import  numpy  as  np
#from numpy.core.fromnumeric import shape
#from scipy.io import wavfile

#### Load Varaible ####
HOST_SIGNAL_FILE  =  "host2.wav"                      # Original file to be watermarked
WATERMARK_SIGNAL_FILE  =  "Signal_USER_1.wav"         # File with embedded watermark
PSEUDO_RAND_FILE  =  'Pseudo_USER_1.dat'              # Pseudo-random number sequence file 
WATERMARK_UNIQUE_FILE  =  'watermark_USER_1.dat'      # Unique watermark signal
WATERMARK_EXTENDED_FILE  =  'watermark_extended.dat'  #extended watermark signal


# set up your variables

                 # Use repeated embedding
FRAME_LENGTH  =  1024              #frame length
CONTROL_STRENGTH  =  0.03          # Embedded strength
OVERLAP  =  0.0                    # Frame analysis overlap rate
NUM_REPS  =  3                     # number of embedded iterations


""" Embed and Extract """
wm.embed(HOST_SIGNAL_FILE,WATERMARK_SIGNAL_FILE,PSEUDO_RAND_FILE,WATERMARK_UNIQUE_FILE,WATERMARK_EXTENDED_FILE,FRAME_LENGTH,CONTROL_STRENGTH,OVERLAP,NUM_REPS )


wm.detect(HOST_SIGNAL_FILE,WATERMARK_SIGNAL_FILE,PSEUDO_RAND_FILE,WATERMARK_UNIQUE_FILE,FRAME_LENGTH,OVERLAP,NUM_REPS  )

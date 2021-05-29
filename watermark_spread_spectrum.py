#!/usr/bin/env python3

"""A python script to perform audio watermark embedding/detection
   on the basis of direct-sequence spread spectrum method."""

#Copyright (C) 2020 by Akira TAMAMORI

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
__name__
import  numpy  as  np
from numpy.core.fromnumeric import shape
from scipy.io import wavfile

#HOST_SIGNAL_FILE  =  "host.wav"                        # Watermark embedding destination file -- Where the watermark will be placeed
#WATERMARK_SIGNAL_FILE  =  "wmed_signal.wav"            # File with embedded watermark -- The wave file witht the embedded information
#PSEUDO_RAND_FILE  =  'pseudo_rand.dat'                 # Pseudo-random number sequence file --- Iautomatically generated
#WATERMARK_UNIQUE_FILE  =  'watermark_ori.dat'        # original watermark signal
#WATERMARK_EXTENDED_FILE  =  'watermark_extended.dat'   #extended watermark signal

#                # Use repeated embedding
#FRAME_LENGTH  =  1024              #frame length
#CONTROL_STRENGTH  =  0.03          # Embedded strength
#OVERLAP  =  0.0                    # Frame analysis overlap rate
#NUM_REPS  =  3                     # number of embedded iterations



def fix(xs):
    """
    A emuration of MATLAB 'fix' function.
    borrowed from https://ideone.com/YjJwOh
    """

    if xs >= 0:
        res = np.floor(xs)
    else:
        res = np.ceil(xs)
    return res


def embed(HOST_SIGNAL_FILE,WATERMARK_SIGNAL_FILE,PSEUDO_RAND_FILE,WATERMARK_UNIQUE_FILE,WATERMARK_EXTENDED_FILE,FRAME_LENGTH,CONTROL_STRENGTH,OVERLAP,NUM_REPS ):
    """ Embed watermark."""
    REP_CODE  =  True                #Use repeated embedding
    #Pseudo random sequence (PRS)
    prs = np.random.rand(1, FRAME_LENGTH) - 0.5
    print(shape(prs))
    # Save pseudo-random number sequence in file
    with open(PSEUDO_RAND_FILE, 'w') as f:
        for d in np.squeeze(prs):
            f.write("%f\n" % d)

   # Open the embedded audio file
    sr, host_signal = wavfile.read(HOST_SIGNAL_FILE)    #host signal has an array
    signal_len  =  len ( host_signal )
    print(signal_len)
    print(host_signal)
    #Frame movement amount (hop_length)
    frame_shift = int(FRAME_LENGTH * (1 - OVERLAP))

    # Overlap length with adjacent frame
    overlap_length = int(FRAME_LENGTH * OVERLAP)

    # Number of bits that can be embedded
    embed_nbit = fix((signal_len - overlap_length) / frame_shift)

    if REP_CODE:
        # Substantial number of embeddable bits
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    # Integerization
    frame_shift = int(frame_shift)
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    #Create original watermark signal (bit string of 0 and 1)
    wmark_unique = np.random.randint(2, size=int(effective_nbit))    # This watermark can be link to the person name

    #Save original watermark signal in a DAT file
    with open(WATERMARK_UNIQUE_FILE, 'w') as f:
        for d in wmark_unique:
            f.write("%d\n" % d)

    # Extend watermark signal
    if REP_CODE:
        wmark_extended = np.repeat(wmark_unique, NUM_REPS)
    else:
        wmark_extended = wmark_unique

    #Save extended watermark signal
    with open(WATERMARK_EXTENDED_FILE, 'w') as f:
        for d in np.squeeze(wmark_extended):
            f.write("%f\n" % d)


    # Generate a watermarked signal
    pointer = 0
    wmed_signal = np.zeros((frame_shift * embed_nbit))  # watermarked signal
    for  i  in  range ( embed_nbit ):
        frame = host_signal[pointer: (pointer + FRAME_LENGTH)]

        alpha = CONTROL_STRENGTH * np.max(np.abs(frame))
        
        print(host_signal)
        print(frame)
        #Embed information according to bit value
        if wmark_extended[i] == 1:
            frame = frame + alpha * prs
        else:
            frame = frame - alpha * prs

        wmed_signal[frame_shift * i: frame_shift * (i+1)] = \
            frame[0, 0:frame_shift]

        pointer = pointer + frame_shift

    wmed_signal = np.concatenate(
        (wmed_signal, host_signal[len(wmed_signal): signal_len]))

    # Save the watermarked signal as wav
    wmed_signal = wmed_signal.astype(np.int16)  # convert float into integer
    wavfile.write(WATERMARK_SIGNAL_FILE, sr, wmed_signal)


def detect(HOST_SIGNAL_FILE,WATERMARK_SIGNAL_FILE,PSEUDO_RAND_FILE,WATERMARK_UNIQUE_FILE,FRAME_LENGTH,OVERLAP,NUM_REPS ):
    """ Detect watermark."""

    # it makes sense to have the following information in the detection procedure 
    # HOST_SIGNAL_FILE => Yes its simply the original file 
    # WATERMARK_SIGNAL_FILE => This is the leaked audio file so yes
    # The Pseudo_file and the WATERMARK_UNIQUE_FILE ARE GOING TO BE TRICKY TO FIND, AS THEY WOULD ESSENTIALLY BE DIFFERENT FOR ALL FILE COPIES


    # Open the embedded audio file
    _, host_signal = wavfile.read(HOST_SIGNAL_FILE)
    
    #Open the embedded audio file
    _, eval_signal = wavfile.read(WATERMARK_SIGNAL_FILE)
    signal_len  =  len ( eval_signal )

    frame_shift = FRAME_LENGTH * (1 - OVERLAP)
    embed_nbit = fix((signal_len - FRAME_LENGTH * OVERLAP) / frame_shift)
    
    REP_CODE  =  True                #Use repeated embedding
    if REP_CODE:
        # Substantial number of embeddable bits
        effective_nbit = np.floor(embed_nbit / NUM_REPS)

        embed_nbit = effective_nbit * NUM_REPS
    else:
        effective_nbit = embed_nbit

    frame_shift = int(frame_shift)
    effective_nbit = int(effective_nbit)
    embed_nbit = int(embed_nbit)

    #Load original watermark signal
    with open(WATERMARK_UNIQUE_FILE, 'r') as f:
        wmark_unique = f.readlines()
    wmark_unique = np.array([int(w.rstrip()) for w in wmark_unique])

    # Load the pseudo-random number sequence used for watermark embedding
    with open(PSEUDO_RAND_FILE, 'r') as f:
        prs = f.readlines()
    rr = np.array([float(x.rstrip()) for x in prs])

    pointer = 0
    detected_bit = np.zeros(embed_nbit)
    for  i  in  range ( embed_nbit ):
        frame = eval_signal[pointer: pointer + FRAME_LENGTH] - \
            host_signal[pointer: pointer + FRAME_LENGTH]

        comp = np.correlate(frame, rr, "full")
        maxp = np.argmax(np.abs(comp))
        if comp[maxp] >= 0:
            detected_bit[i] = 1
        else:
            detected_bit[i] = 0

        pointer = pointer + frame_shift

    if REP_CODE:
        count = 0
        wmark_recovered = np.zeros(effective_nbit)

        for  i  in  range ( effective_nbit ):
            ave = np.sum(detected_bit[count:count+NUM_REPS]) / NUM_REPS

            if ave >= 0.5:
                wmark_recovered[i] = 1
            else:
                wmark_recovered[i] = 0

            count = count + NUM_REPS
    else:
        wmark_recovered = detected_bit

    #Display bit error rate
    BER = np.sum(np.abs(wmark_recovered - wmark_unique)) / \
        effective_nbit * 100
    print(f'bit error rate = {BER} %')

    # SNR
    SNR = 10 * np.log10(
        np.sum(np.square(host_signal.astype(np.float32)))
        / np.sum(np.square(host_signal.astype(np.float32)
                           - eval_signal.astype(np.float32))))
    #print(f'SNR = {SNR}dB')


#def main():
    """Main routine. """

    #embed ()                      # Watermark embedding
    #detect ()                     # Watermark detection


#if __name__ in '__main__':
    #main()

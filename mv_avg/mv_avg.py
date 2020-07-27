#---------------------------------------------
#moving average filter
#by ramona a •w•          implements a moving average filter
#7-25-20                  using output-side convolution         
#><>|^*^|<><              ----------------------------------------------------------------------------------     
#_______                  • input signal    x[n]:   (dataSize) samples    
#--___--                  • filter kernel   h[m]:   45 samples (m) (centered)
#  |||___-π-___...        • bit depth:      bps:    8 [0-255] bits
#  |||---|||---|||        • the impulse response h[n] is a rectangular pulse of depth 1/m
# / π \       / π \         spanning the width of the filter kernel (45 samples)
# \___/       \___/       • in this case, since the impulse response h[n] == 1/m for every sample,
#                           the multiplication of 1/m by each input sample is factored out of the summation
#                           giving: y[n] == 1/m * Σx[n] | [-22, 22]
#                         • for each output sample [22 - (dataSize - 23)], the range [-22, 22] of x[n]
#                           around the center point n is summed (accumulated), then divided by 45
#                         • giving a fully immersed output y[n] of length (dataSize -  44) 
#                           • padded with 22 zeroes on either end - necessary for full immersion
#---------------------------------------------
import struct

# open waveform input & output files for reading & writing, respectively
# read the header chunks of the input wav & copy to output wav (prep for write)
# get relevant metadata from input wav 
#    # of channels, sampling frequency, bits per sample, byte rate, data chunk size
#------------------------------------------------------------------------

inputSignal = open("sample.wav", mode = "rb", buffering = 0)    #open input signal file for read (raw)
outputSignal = open("output.wav", mode = "wb")                  #open output signal file for write                    

headerChunks = inputSignal.read(44)     #read header chunk from input signal (first 44 bytes)
outputSignal.write(headerChunks)        #copy header chunk to output signal (for wav formatting)

nChan = struct.unpack("<H", headerChunks[22:24])[0]     #read # of channels as uShort (LE)
sFreq = struct.unpack("<L", headerChunks[24:28])[0]     #read sampling frequency as uLong (LE)
bps   = struct.unpack("<H", headerChunks[34:36])[0]     #read bits per sample as uShort (LE)
BRate = struct.unpack("<L", headerChunks[28:32])[0]     #read byte rate (Bps) as uLong (LE)
                                                            #calculated as (nChan * sFreq * bps)/8
dataSize = struct.unpack("<L", headerChunks[40:44])[0]  #total size of sample data in bytes (LE)
                                                            #calculated as (nSamp * nChan * bps)/8
print("")
print("------------------")
print("channels: %s | sFreq: %s samples/sec | depth: %s bits | Bps: %s bytes/sec" % (nChan, sFreq, bps, BRate))
print("size: %s samples" % dataSize)
print("")

# moving average filter implementation
# using output-side convolution
#   45 point impulse response (centered)
#   n = [22, (dataSize - 1) - 22]
#   M = 45
#   h[x] = 1/M = 1/45 for all points
#   y[n] = 1/45(Σx[n + m] | m = [-22, 22]
#---------------------------------------------
inputWave = inputSignal.read()      #read rest of wav data into bytes object (from index 44)

for initOut in range(0, 22):        #for initOut = [0, 21] - loop 22 times - (full immerision)
    outputSignal.write(bytes(1))        #write null bytes object of size 1 to file

for n in range(22, (dataSize - 22)):#for n = [22, datasize - 23] - loop thru input samples
    outputSample = 0                    #initialize accumulator
    for m in range(-22, 23):            #for m = [-22, 22] - loop thru input window
        outputSample += inputWave[n + m]    #accumulate input samples
    outputSample /= 45                  #average input samples (factored impulse response)
    outputSample = int(outputSample)    #convert average to int to compute output sample
    
    outputByte = bytearray(1)           #create new bytearray object of size 1
    outputByte[0] = outputSample        #write output sample to bytearray
    outputSignal.write(outputByte)      #write byte to file
    
for finishOut in range(0, 22):      #finishOut = [0, 21] - loop 22 times (full immersion)
    outputSignal.write(bytes(1))        #write null bytes object of size 1 to file
    
outputSignal.close()                #close output file
inputSignal.close()                 #close input file
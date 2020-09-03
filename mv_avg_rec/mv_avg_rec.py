#---------------------------------------------
#moving average filter
#by ramona a •w•          
#7-25-20                  implements a moving average filter using recursion, requiring only
#                         2 additions per sample (as opposed to M additions for pure convolution)
#                         frequency response is a sinc function H[f] = sin(πfM)/Msin(πf), with f | [0, .5]
#><>|^*^|<><              ----------------------------------------------------------------------------------     
#_______                  • input signal    inputWave[n]:       (dataSize) samples    
#--___--                  • filter kernel   h[m]                45 samples (M) (centered)
#  |||___-π-___...        • bit depth:      bps:                8 bits [0-255]
#  |||---|||---|||        • the impulse response h[m] is a rectangular pulse of depth 1/M
# / π \       / π \         spanning the full width of the filter kernel (M == 45 samples)
# \___/       \___/       • in this case, since the impulse response h[m] == 1/M for every sample m,
#                           the multiplication of 1/M by each input sample is factored out of the summation
#                           giving: y[n] == 1/m * Σx[n] | n = [-22, 22]
#                         • since Σx[n] differs from Σx[n - 1] by only two terms (L & R boundaries)
#                           the previously accumulated sum Σx[n - 1] can be converted into the current
#                           sum Σx[n] by subtracting sample x[n - 22] and adding sample x[n + 23]
#                         • multiplying the newly calculated sum by (1/M) gives the output sample y[n]
#                         • this progam yields a fully immersed output y[n] of length (dataSize -  44) 
#                           • padded with 22 zeroes on either end
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
# using recursion
# 45 point impulse response (symmetrical around [-(M - 1)/2, (M - 1)/2])
#---------------------------------------------
inputWave = inputSignal.read()      #read rest of wav data into bytes object (from index 44)

for initOut in range(0, 22):        #for initOut = [0, 21] - loop 22 times - (full immersion)
    outputSignal.write(bytes(1))        #write 22 null bytes objects of size 1 to file

outputAcc = 0                       #initialize accumulator
for m in range(-22, 23):            #calculate first output sample from inputWave[0, 44]
    outputAcc += inputWave[22 + m]      #accumulate 45 input samples
outputSample = int(outputAcc/45)    #average input samples and cast result to int

outputByte = bytearray(1)           #create new bytearray object of size 1
outputByte[0] = outputSample        #write first output sample to bytearray
outputSignal.write(outputByte)      #write byte to file

for n in range(23, (dataSize - 22)):#for n = [23, datasize - 23] - skip first sample
    outputAcc = (outputAcc - inputWave[n - 23] + inputWave[n + 22]) #recalculate accumulator using previous value
    outputSample = int(outputAcc/45)    #average updated accumulator samples to calculate new output
    
    outputByte = bytearray(1)           #create new bytearray object of size 1
    outputByte[0] = outputSample        #write output sample to bytearray
    outputSignal.write(outputByte)      #write byte to file
    
for finishOut in range(0, 22):      #finishOut = [0, 21] - loop 22 times - (full immersion)
    outputSignal.write(bytes(1))        #write null bytes object of size 1 to file
    
outputSignal.close()                #close output file
inputSignal.close()                 #close input file
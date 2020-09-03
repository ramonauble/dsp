---------------------------------------------
explorations
by ramona a •w•                      ←-___←↑→__-→
9-3-20                              ←-///π\//π \\-→
><>|^*^|<><                         ←-\\π↓|↑|↓π//-→
_______                              ←-\\π+r+π//-→
--___--                               ←-\\π+π//-→
  |||___-π-___...                      ←-\\↑//-→
  |||---|||---|||                       ←-\π/-→
 / π \       / π \                       ←-|-→
 \___/       \___/                        ←↓→
---------------------------------------------------
              DSP tests & studies
---------------------------------------------------

• mv_avg - 45 point moving average filter using convolution
  • this program takes a mono 8bit wav file of arbitary length as input
  • uses output side convolution to implement a moving average filter
    with a 45 point impulse response
  • applies the algorithm to the entire input waveform, storing the filtered
    output as a new wav file in the same directory
  • reads/writes the wav file directly (does not use Lib/wave.py module)
  
• mv_avg_rec - 45 point moving average filter using recursion
  • this program takes a mono 8bit wav file of arbitary length as input
  • uses recursive convolution to calculate output samples from prior outputs
    eliminating the need for M - 2 additions every output sample
  • applies the algorithm to the entire input waveform, storing the filtered
    output as a new wav file in the same directory
  • reads/writes the wav file directly
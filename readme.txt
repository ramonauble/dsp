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
---------------------------------------------------

• mv_avg - moving average filter by convolution
  • this program takes a mono 8bit wav file of arbitary length as input
  • the output samples are calculated by convolving the input signal
    with a 45 point impulse response equal to 1/45 at all points
  • applies the algorithm to the entire input waveform, storing the filtered
    output as a new wav file in the same directory
  
• mv_avg_rec - moving average filter by recursive convolution
  • this program takes a mono 8bit wav file of arbitary length as input
  • by recursion, the output samples are calculated from prior outputs,
    averting the need for M - 2 additions every output sample
    ♪ still requires one multiplication
  • applies the algorithm to the entire input waveform, storing the filtered
    output as a new wav file in the same directory
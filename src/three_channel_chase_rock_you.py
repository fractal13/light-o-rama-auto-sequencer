#!/usr/bin/env python3
import lorxml
import loraubio
import sys
import os

def debounce(beats_in, limit):
    last = 0
    beats_out = []
    for beat in beats_in:
        if beat - last < limit:
            pass
        else:
            beats_out.append(beat)
            last = beat
    return beats_out

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename="../../Queen.1977.News_Of_The_World_(CDP_746209_2).01.We_Will_Rock_You.mp3"
    short_filename = "Queen.1977.News_Of_The_World_(CDP_746209_2).01.We_Will_Rock_You.mp3"

    if not os.path.exists(filename):
        print( filename + " does not exist." )
        sys.exit(1)

    total_time = loraubio.find_total_time(filename)
    if len(sys.argv) > 2:
        if sys.argv[2] == 'beats':
            beats = loraubio.find_beats(filename)
        elif sys.argv[2] == 'onsets':
            beats = loraubio.find_onsets(filename)
        elif sys.argv[2] == 'notes':
            notes = loraubio.find_notes(filename)
            beats = [ x[0] for x in notes ]
        else:
            print("only beats, onests, notes understood")
            sys.exit(1)
    else:
        beats = loraubio.find_beats(filename)

    beats = debounce(beats, 20)
                
    s = lorxml.Sequence()
    s.addMusicFile(short_filename)
    i = s.addChannel("A: 3.1", 3, 1)
    j = s.addChannel("B: 3.2", 3, 2)
    k = s.addChannel("C: 3.3", 3, 3)
    channel_indexes = [i, j, k]

    intensity = 100
    i = 0
    last_beat = 0
    for beat in beats:
        s.addConstantEffect( channel_indexes[i], "intensity", last_beat, beat, intensity )
        i += 1
        i %= len(channel_indexes)
        last_beat = beat

    tg_0 = s.addFreeFormTimingGrid("beats")
    s.addTrack(total_time, tg_0)

    s.write("three_channel_chase_rock_you.las")
    return

if __name__ == "__main__":
    main()
    

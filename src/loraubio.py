#!/usr/bin/env python3

import aubio

def find_total_time(filename):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0
    source = aubio.source(filename, samplerate, hop_s)
    total_time = int(100*source.duration/source.samplerate)
    return total_time

def find_notes(filename):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0

    source = aubio.source(filename, samplerate, hop_s)
    samplerate = source.samplerate
    notes_o = aubio.notes("default", win_s, hop_s, samplerate)
    
    notes = []
    
    total_frames = 0
    while True:
        samples, read = source()
        new_note = notes_o(samples)
        if new_note[0] != 0:
            note_time = int(100*total_frames/float(samplerate))
            this_note = (note_time, new_note[0], new_note[1], new_note[2])
            notes.append(this_note)
        total_frames += read
        if read < hop_s: break
    return notes

def find_onsets(filename):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0

    source = aubio.source(filename, samplerate, hop_s)
    samplerate = source.samplerate
    onset = aubio.onset("default", win_s, hop_s, samplerate)
    
    onsets = []
    
    total_frames = 0
    while True:
        samples, read = source()
        is_onset = onset(samples)
        if is_onset:
            this_onset = onset.get_last()
            onsets.append(int(100*this_onset/source.samplerate))
        total_frames += read
        if read < hop_s: break
    return onsets

def find_beats(filename):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0

    source = aubio.source(filename, samplerate, hop_s)
    samplerate = source.samplerate
    # print(source)
    # print(source.samplerate)
    # print(source.duration)
    # print(source.duration/source.samplerate)
    # print(source.channels)
    # #print(source.__dir__())

    tempo = aubio.tempo("default", win_s, hop_s, samplerate)
    delay = 4. * hop_s
    
    beats = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = source()
        is_beat = tempo(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            beats.append(int(100*this_beat/source.samplerate))
        total_frames += read
        if read < hop_s: break
    return beats

def main():
    filename="../../Queen.1977.News_Of_The_World_(CDP_746209_2).01.We_Will_Rock_You.mp3"

    beats = find_beats(filename)
    print( len(beats) )
    for beat in beats:
        print(beat)
    return

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import lorxml

def main():
    s = lorxml.Sequence()
    i = s.addChannel("A: 3.1", 3, 1)
    j = s.addChannel("B: 3.2", 3, 2)
    k = s.addChannel("C: 3.3", 3, 3)

    lorxml.add_chase(s, [i,j,k],          0, 1000,  33, 100)
    lorxml.add_chase(s, [k,j,i],       1000, 2000,  66,  50)
    lorxml.add_chase(s, [i,j,k,j,k,k], 2000, 4000,  10,  75)

    s.write("three_channel_chase.xml")
    return

if __name__ == "__main__":
    main()
    

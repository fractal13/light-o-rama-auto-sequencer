#!/usr/bin/env python3
#
# XML processing for the Light-o-Rama sequence file.
#
import xml.etree.ElementTree
import xml.dom.minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = xml.etree.ElementTree.tostring(elem, 'utf-8')
    #return rough_string
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

class Channel:

    def __init__(self, name, unit, circuit, saved_index):
        self.name = name
        self.color = "12615744"
        self.centiseconds = 0
        self.deviceType = "LOR"
        self.unit = unit
        self.circuit = circuit
        self.savedIndex = saved_index
        return

    def setCentiSeconds(self, centiseconds):
        self.centiseconds = centiseconds
        return

    def toElement(self):
        attributes = { "name": str(self.name),
                       "color": str(self.color),
                       "centiseconds": str(self.centiseconds),
                       "deviceType": str(self.deviceType),
                       "unit": str(self.unit),
                       "circuit": str(self.circuit),
                       "savedIndex": str(self.savedIndex) }
        e = xml.etree.ElementTree.Element("channel", attributes)
        return e

class Channels:

    def __init__(self):
        self.channel_list = {}
        self.next_index = 0
        return

    def addChannel(self, name, unit, circuit):
        saved_index = self.next_index
        channel = Channel(name, unit, circuit, saved_index)
        self.channel_list[saved_index] = channel
        self.next_index += 1
        return

    def toElement(self):
        attributes = {}
        e = xml.etree.ElementTree.Element("channels", attributes)
        for saved_index in self.channel_list:
            c = self.channel_list[saved_index].toElement()
            e.append(c)
        return e

class Sequence:

    def __init__(self):
        self.saveFileVersion = 14
        self.author = "cgl"
        self.createdAt = "11/08/2019 2:00:00 PM"
        self.musicFilename = "foo.mp3"
        self.videoUsage = "2"
        self.channels = Channels()
        return

    def addChannel(self, name, unit, circuit):
        return self.channels.addChannel(name, unit, circuit)

    def toElement(self):
        attributes = { "saveFileVersion": str(self.saveFileVersion),
                       "author": str(self.author),
                       "createdAt": str(self.createdAt),
                       "musicFilename": str(self.musicFilename),
                       "videoUsage": str(self.videoUsage) }
        e = xml.etree.ElementTree.Element("sequence", attributes )
        e.append(self.channels.toElement())
        return e

    def write(self, filename):
        e = self.toElement()
        fout = open(filename, "w")
        fout.write(prettify(e))
        fout.close()
        return
    
def main():
    s = Sequence()
    s.addChannel("A: 3.1", 3, 1)
    s.addChannel("B: 3.2", 3, 2)
    s.addChannel("C: 3.3", 3, 3)
    s.addChannel("D: 3.4", 3, 4)
    s.write("sample.xml")
    return

if __name__ == "__main__":
    main()

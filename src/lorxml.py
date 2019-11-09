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

# available types = { intensity, shimmer, twinkle }

class Effect:

    def __init__(self, effect_type, start_centisecond, end_centisecond):
        self.type = effect_type
        self.startCentisecond = start_centisecond
        self.endCentisecond = end_centisecond
        return

    def toElement(self,attribs={}):
        attributes = { "type": str(self.type),
                       "startCentiSecond": str(self.startCentisecond),
                       "endCentiSecond": str(self.endCentisecond) }
        attributes.update(attribs)
        e = xml.etree.ElementTree.Element("effect", attributes)
        return e

class ConstantEffect(Effect):

    def __init__(self, effect_type, start_centisecond, end_centisecond, intensity):
        super().__init__(effect_type, start_centisecond, end_centisecond)
        self.intensity = intensity
        return

    def toElement(self):
        attributes = { "intensity": str(self.intensity) }
        return Effect.toElement(self,attributes)

class VariableEffect(Effect):

    def __init__(self, effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity):
        super().__init__(effect_type, start_centisecond, end_centisecond)
        self.startIntensity = start_intensity
        self.endIntensity = end_intensity
        return

    def toElement(self):
        attributes = { "startIntensity": str(self.startIntensity),
                       "endIntensity": str(self.endIntensity) }
        return Effect.toElement(self,attributes)

class Channel:

    def __init__(self, name, unit, circuit, saved_index):
        self.name = name
        self.color = "12615744"
        self.centiseconds = 0
        self.deviceType = "LOR"
        self.unit = unit
        self.circuit = circuit
        self.savedIndex = saved_index
        self.effect_list = []
        return

    def addConstantEffect(self, effect_type, start_centisecond, end_centisecond, intensity):
        effect = ConstantEffect(effect_type, start_centisecond, end_centisecond, intensity)
        self.effect_list.append(effect)
        return

    def addVariableEffect(self, effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity):
        effect = VariableEffect(effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity)
        self.effect_list.append(effect)
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
        for effect in self.effect_list:
            e.append(effect.toElement())
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
        return saved_index

    def addConstantEffect(self, channel_index, effect_type, start_centisecond, end_centisecond, intensity):
        return self.channel_list[channel_index].addConstantEffect(effect_type, start_centisecond, end_centisecond, intensity)

    def addVariableEffect(self, channel_index, effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity):
        return self.channel_list[channel_index].addVariableEffect(effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity)

    def toElement(self):
        attributes = {}
        e = xml.etree.ElementTree.Element("channels", attributes)
        for saved_index in self.channel_list:
            c = self.channel_list[saved_index].toElement()
            e.append(c)
        return e

class TimingGrids:

    def __init__(self):
        return

    def toElement(self):
        attributes = {}
        e = xml.etree.ElementTree.Element("timingGrids", attributes)
        return e

class Tracks:

    def __init__(self):
        return

    def toElement(self):
        attributes = {}
        e = xml.etree.ElementTree.Element("tracks", attributes)
        return e
    
class Animation:

    def __init__(self):
        return

    def toElement(self):
        attributes = { "rows": str(40), "columns": str(50), "image": "" }
        e = xml.etree.ElementTree.Element("animation", attributes)
        return e

class Sequence:

    def __init__(self):
        self.saveFileVersion = 14
        self.author = "cgl"
        self.createdAt = "11/08/2019 2:00:00 PM"
        self.musicFilename = "foo.mp3"
        self.videoUsage = "2"
        self.channels = Channels()
        self.timing_grids = TimingGrids()
        self.tracks = Tracks()
        self.animation = Animation()
        return

    def addChannel(self, name, unit, circuit):
        return self.channels.addChannel(name, unit, circuit)

    def addConstantEffect(self, channel_index, effect_type, start_centisecond, end_centisecond, intensity):
        return self.channels.addConstantEffect(channel_index, effect_type, start_centisecond, end_centisecond, intensity)

    def addVariableEffect(self, channel_index, effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity):
        return self.channels.addVariableEffect(channel_index, effect_type, start_centisecond, end_centisecond, start_intensity, end_intensity)

    def toElement(self):
        attributes = { "saveFileVersion": str(self.saveFileVersion),
                       "author": str(self.author),
                       "createdAt": str(self.createdAt),
                       "musicFilename": str(self.musicFilename),
                       "videoUsage": str(self.videoUsage) }
        e = xml.etree.ElementTree.Element("sequence", attributes )
        e.append(self.channels.toElement())
        e.append(self.timing_grids.toElement())
        e.append(self.tracks.toElement())
        e.append(self.animation.toElement())
        return e

    def write(self, filename):
        e = self.toElement()
        fout = open(filename, "w")
        fout.write(prettify(e))
        fout.close()
        return
    
def main():
    s = Sequence()
    i = s.addChannel("A: 3.1", 3, 1)
    j = s.addChannel("B: 3.2", 3, 2)
    k = s.addChannel("C: 3.3", 3, 3)
    l = s.addChannel("D: 3.4", 3, 4)

    s.addConstantEffect(i, "intensity", 0, 95, 78)
    s.addConstantEffect(i, "intensity", 95, 200, 64)
    s.addConstantEffect(i, "shimmer", 300, 500, 100)
    s.addVariableEffect(i, "intensity", 500, 1000, 100, 0)
    
    s.write("sample.xml")
    return

if __name__ == "__main__":
    main()

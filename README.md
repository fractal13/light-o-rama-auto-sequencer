Light-O-Rama Auto Sequencer
---------------------------

This tool is intended to automatically creates sequences for
the Light-O-Rama system.  It will use a library such
as [aubio](https://github.com/fractal13/aubio) to read audio
files, and process them, looking for audio events such
as overall beats, or attacks by various instruments or voices.
These event timings will be used to create a set of LOR timing 
grids.  Finally, the timing grids will be used to generate
interesting lighting patterns for the channels of the controllers
and they will be written out in the LOR compatible sequence files.

Documentation on Audio Processing with `aubio`
------------------------------------------

Should provide some documentation or at least samples of use here.

Documentation on XML Processing with `??`
-----------------------------------------
    
Should provide some documentation or at least samples of use here.
[ElementTree](https://docs.python.org/3.6/library/xml.etree.elementtree.html)


Structure of a Light-O-Rama Sequence File
-----------------------------------------

These files use the extension `.lms`, the underlying format is
XML. The XML structure is documented here, to the best of our
ability, using samples created by the LOR Sequencer software.

    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!--- saveFileVersion="14" appears to be standard --->
    <!--- author="string" appears to be the user who created the sequence --->
    <!--- createdAt="mm/dd/yyyy h:mm:ss PM" is the time --->
    <!--- musicFilename="file.wav" the name of the file, if it is stored in the Audio/ sub folder for LOR --->
    <!--- videoUsage="2" appears to be standard, I don't know why --->
    <!--- musicAlbum="string" is optional --->
    <!--- musicArtist="string" is optional --->
    <!--- musicTitle="string" is optional --->
    <sequence saveFileVersion="14" author="Katelyn" createdAt="11/30/2016 3:54:20 PM" musicFilename="Gene-Autry-Jingle-Bells-Trimmed.wav" videoUsage="2">
      <!--- The list of all channels that are controlled for this sequence --->
      <channels>
          <!--- name="string" is a display name in the LOR GUI --->
          <!--- color="string" is a display color in the LOR GUI --->
          <!--- centiseconds="number" is the number of centiseconds this channel is active.  usually the length of the song --->
          <!--- deviceType="LOR" for all of my LOR controllers --->
          <!--- unit="number" the LOR controller configured number --->
          <!--- circuit="number" the LOR controller's port number for this channel --->
          <!--- savedIndex="number" an internal indexing number to refer to this channel --->
          <channel name="Unit 01.1" color="12615744" centiseconds="11683" deviceType="LOR" unit="1" circuit="1" savedIndex="0">
              <!--- type="intensity" the type of effect for this channel --->
              <!---       intensity, shimmer, twinkle, ... --->
              <!--- startCentisecond="number" when to start this effect --->
              <!--- endCentisecond="number" when to finish this effect --->
              <!--- intensity="number" 0 to 100, how bright to make this effect --->
              <!--- startIntensity="number" 0 to 100, how bright to make this effect at the beginning --->
              <!--- endIntensity="number" 0 to 100, how bright to make this effect at the end --->
		      <effect type="intensity" startCentisecond="1077" endCentisecond="1104" intensity="100"/>
			  <effect type="intensity" startCentisecond="4142" endCentisecond="4180" startIntensity="100" endIntensity="0"/>
              <!--- ... more effects ... --->
          </channel>
          <!--- ... more channels ... --->
      </channels>
      <!--- timing grids to be displayed in the LOR GUI, maybe not required? Certainly helpful to fine-tune the result manually in LOR's GUI --->
	  <timingGrids>
          <!--- saveID="number" 0 to N, the grid's order --->
          <!--- name="string" display name of the grid --->
          <!--- type="freeform" for non-regular grids, those based on data --->
	      <timingGrid saveID="0" name="Choir beginning" type="freeform">
              <!--- centisecond="number" time into the song where the grid line starts --->
	          <timing centisecond="1270"/>
              <!--- ... more timing entries ... --->
	      </timingGrid>
          <!--- a fixed timing grid example --->
	      <timingGrid saveID="9" name="Fixed Grid: 0.10" type="fixed" spacing="10"/>
          <!--- ... more timing grids ... --->
      </timingGrids>
      <!--- not sure how tracks work. maybe you can put multiple songs in the same sequence? --->
      <tracks>
          <!--- totalCentiseconds="number" appears to be the song length --->
          <!--- timingGrid="number" there were timing grids with saveID 0 through 12 in this example, I think this is the id of the "active" grid in the GUI --->
          <track totalCentiseconds="11683" timingGrid="12">
	          <channels>
	              <channel savedIndex="62"/>
                  <!--- ... all channels used for this track ... --->
	          </channels>
	          <loopLevels/>
	      </track>
          <!--- ... more tracks? ... --->
      </tracks>
      <animation rows="40" columns="60" image=""/>
    </sequence>


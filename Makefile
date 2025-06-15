# Convert ABC files to MP3 via MIDI

ABCFILES := $(wildcard *.abc)
MIDIFILES := $(ABCFILES:.abc=.mid)
MP3FILES := $(ABCFILES:.abc=.mp3)

%.mid: %.abc
	abc2midi $< -o $@

%.mp3: %.mid
	timidity $< -Ow -o - | lame - $@

.PHONY: all clean

all: $(MP3FILES)

clean:
	rm -f *.mid *.mp3

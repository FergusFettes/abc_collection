# Convert ABC files to MP3 via MIDI

ABCFILES := $(wildcard *.abc)
MIDIFILES := $(ABCFILES:.abc=.mid)
MP3FILES := $(ABCFILES:.abc=.mp3)

%.mid: %.abc
	abc2midi $< -o $@

%.mp3: %.mid
	timidity $< -Ow -o - | lame - $@

%: %.mp3
	@echo "Created $<"

%-in-c.abc: %.abc
	abc2abc $< -t -7 > $@

.PHONY: all clean transpose

all: $(MP3FILES)

# Usage: make transpose FILE=songname (without .abc extension)
transpose:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make transpose FILE=songname (without .abc extension)"; \
		exit 1; \
	fi
	@if [ ! -f "$(FILE).abc" ]; then \
		echo "Error: $(FILE).abc does not exist"; \
		exit 1; \
	fi
	make $(FILE)-in-c.abc

clean:
	rm -f *.mid *.mp3 *-in-c.abc

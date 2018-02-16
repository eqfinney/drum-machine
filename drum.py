#
# Drum Machine Code
#

import sys
import time


class Song:

    def __init__(self, title, bpm):
        """
        Initiates the Song object.
        Input: title (string), the title of the song
               bpm (int), the number of beats to be played per minute
               tempo_step (float), the time it takes to play each step
                   Note there are two steps per beat for this song, as per the README
               patterns (dictionary), maps a pattern name to a bitmap of its rhythm
        """
        self.title = title
        self.bpm = bpm
        # from the README: note for an eight-count bar (4/4 time signature),
        # there should be 256 counts per minute (128 beats per minute)
        self.tempo_step = ((60/self.bpm)*4)/8
        self.patterns = {}

    def add_pattern(self, pattern_name, pattern):
        """
        Adds a pattern to the song object. This allows us to layer the song as necessary.
        Input: drum_name (string), the name of the drum sound to be played
               pattern (string), a bitmap of the rhythm the drum should produce
        """
        self.patterns[pattern_name] = pattern

    def one_count_gen(self):
        """
        Generates one count of the rhythm, combining all instruments into a coherent output
        Output: beat_string (string), a string representing which instruments are played
                   during that count of the rhythm. Instruments should be named in output.
        """
        beat = 0

        while True:
            beat_string = "| "

            # make the song happen
            for pattern_name, pattern_type in self.patterns.items():
                pattern_length = len(pattern_type)
                # indexing by beat % pattern_length allows us to easily play rhythms
                # that are different lengths (e.g., 8 beats and 16 beats) simultaneously
                if pattern_type[ beat % pattern_length ] == "1":
                    if beat_string == "| ":
                        beat_string += pattern_name + " "
                    else:
                        beat_string += "+ " + pattern_name + " "

            if beat_string == "| ":
                beat_string += "X "

            # this function uses Python's generators
            # generators allow the function to pause while it yields output
            # but saves the function's stack frame so it can be easily called again
            # e.g., the generator could be called at the next beat with no new setup
            yield beat_string

            beat += 1


def play(song, stop_time):
    """
    This function plays a song whose information has been stored in a step-by-step
    generator. The function not included as a method of the Song class to allow
    different songs to be more easily mixed, a common characteristic of the EDM for
    which drum machines are commonly used.
    Input: song (Song object), an object containing information about a song's title,
               speed/tempo, and any drum patterns that have been added to the music
           stop_time (int), the number of seconds after which to stop playing the song
    Output: none, but the song's beat should be printed to stdout in the command line
    """

    print("Playing a new song!")
    print("Song Title: ", song.title)
    print("Song Speed: ", song.bpm)

    start_time = time.time()
    current_time = 0

    # initialize the song's generator
    beat_generator = song.one_count_gen()

    while current_time < stop_time:
        # update the current time to keep track of how long the song has been playing
        current_time = time.time() - start_time
        # produce the next step of the song. Note: may not be equal to one beat
        new_step = next(beat_generator)
        time.sleep(song.tempo_step)
        sys.stdout.write("%s" % new_step)
        sys.stdout.flush()


if __name__ == "__main__":
    # use bitmaps to encode the drum patterns
    # a "1" represents that the instrument should produce sound
    # a "0" represents that the instrument should be quiet
    pattern_dict = {"kick": "10001000", "snare": "00001000", "hihat": "00100010",
                    "cowbell": "0000001000100010"}

    # like Animal Rights, but with a cowbell
    animal_rights_remix = Song(title="Animal Rights: fedcow5 & Bovine Gardener Remix", bpm=128)
    for name, rhythm in pattern_dict.items():
        animal_rights_remix.add_pattern(name, rhythm)

    play(animal_rights_remix, stop_time=15)

from pygame import mixer

# Starting the mixer
mixer.init()


class Audio:
    _sounds = {
        'swipe': mixer.Sound('assets/swipe.wav'),
        'error': mixer.Sound('assets/blocked.wav'),
        'combine': mixer.Sound('assets/combine.wav'),
        'explode': mixer.Sound('assets/explode.wav'),
        'gameover': mixer.Sound('assets/gameover.wav')
    }

    @staticmethod
    def play_sound(name):
        try:
            sound = Audio._sounds[name]
            sound.play(0)
        except KeyError:
            print("Trying to play unknown sound: " + str(name))

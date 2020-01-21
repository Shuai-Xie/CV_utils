"""
Finite State Machine: https://github.com/pytransitions/transitions
"""

from transitions import Machine
import random


class NarcolepticSuperhero:
    # 嗜睡的 superhero
    states = ['asleep', 'hanging out', 'hungry', 'sweaty', 'saving the world']

    def __init__(self, name):
        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name

        # What have we accomplished today?
        self.kittens_rescued = 0

        # Initialize the state machine
        # set NarcolepticSuperhero.state in `Machine.set_state()`
        self.machine = Machine(model=self, states=NarcolepticSuperhero.states, initial='asleep')

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        # source --> trigger --> dest
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='hanging out')
        self.machine.add_transition('work_out', 'hanging out', 'hungry')  # 健身
        self.machine.add_transition('eat', 'hungry', 'hanging out')

        # before,after,conditions: pass in funcs defined in class

        # Superheroes are always on call. ALWAYS.
        # But they're not always dressed in work-appropriate clothing.
        self.machine.add_transition('distress_call', '*', 'saving the world',
                                    before='change_into_super_secret_costume')
        # saving the world -> 登记救下的 kittens
        self.machine.add_transition('complete_mission', 'saving the world', 'sweaty',
                                    after='update_journal')

        # Sweat is a disorder that can be remedied with water.
        # Unless you've had a particularly long day, in which case... bed time!
        # 满足 is_exhausted 条件，才会进入 asleep
        self.machine.add_transition('clean_up', 'sweaty', 'asleep', conditions=['is_exhausted'])
        self.machine.add_transition('clean_up', 'sweaty', 'hanging out')

        # Our NarcolepticSuperhero can fall asleep at pretty much any time.
        self.machine.add_transition('nap', '*', 'asleep')

    def update_journal(self):
        """ Dear Diary, today I saved Mr. Whiskers. Again. """
        self.kittens_rescued += 1

    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")


if __name__ == '__main__':
    batman = NarcolepticSuperhero("Batman")
    print(batman.state)
    batman.wake_up()  # a str in states is a property of fsm
    print(batman.state)


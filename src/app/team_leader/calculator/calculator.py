from .headline import HeadlineCalculator
from .third import ThirdCalculator
from .answering_machine import AnsweringMachineCalculator

class Calculator(object):
    def get_evaluation(self, args):
        if args == 'headline':
            return HeadlineCalculator
        elif args == 'third':
            return ThirdCalculator
        elif args == 'answering_machine':
            return AnsweringMachineCalculator

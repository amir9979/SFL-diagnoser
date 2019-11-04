import copy
import math
import random
from math import ceil
import Diagnosis
import sfl_diagnoser.Diagnoser.dynamicSpectrumOptimize
from sfl_diagnoser.Diagnoser.Experiment_Data import Experiment_Data
import sfl_diagnoser.Planner.domain_knowledge
import numpy
import sfl_diagnoser.Diagnoser.diagnoserUtils
from sfl_diagnoser.Diagnoser.Singelton import Singleton
import sfl_diagnoser.Diagnoser.ExperimentInstance

TERMINAL_PROB = 0.7


class Instances_Management(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.instances = {}
        self.clear()

    def clear(self):
        self.instances.clear()
        self.instances = {}

    def get_instance(self, initial_tests, error):
        key = repr(sorted(initial_tests)) + "-" + repr(sorted(map(lambda x: x[0], filter(lambda x: x[1] == 1, error.items()))))
        if key not in self.instances:
            self.instances[key] = self.create_instance_from_key(key)
        return self.instances[key]

    def create_instance_from_key(self, key):
        initial, failed = key.split('-')
        error = dict([(i, 1 if i in eval(failed) else 0) for i in Experiment_Data().POOL])
        return ExperimentInstanceOptimize(eval(initial), error)


class ExperimentInstanceOptimize(sfl_diagnoser.Diagnoser.ExperimentInstance.ExperimentInstance):
    def __init__(self, initial_tests, error):
        super(ExperimentInstanceOptimize, self).__init__(initial_tests, error)

    def _create_ds(self):
        return sfl_diagnoser.Diagnoser.dynamicSpectrumOptimize.dynamicSpectrumOptimize()

    def create_instance(self, initial_tests, error):
        return Instances_Management().get_instance(initial_tests, error)

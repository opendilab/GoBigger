import os
import logging
import pytest
import uuid
from pygame.math import Vector2
import pygame
import random
import numpy as np
import cv2

from gobigger.utils import SequenceGenerator

logging.basicConfig(level=logging.DEBUG)


def test_sequence_generator():
    class Temp:
        def __init__(self, sequence_generator=None):
            self.sequence_generator = sequence_generator
        def generate(self):
            return self.sequence_generator.get()
    sequence_generator = SequenceGenerator(0)
    ts = [Temp(sequence_generator) for i in range(5)]
    for index, t in enumerate(ts):
        assert t.generate() == index

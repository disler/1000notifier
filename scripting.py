import inspect
import sys
from strategy import strategy


inst = strategy.create_strategy_instance("StrategyVolumeChange", {'increase_ratio': 1.5})

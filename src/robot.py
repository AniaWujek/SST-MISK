"""
Script responsible for managing single robot.
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from wrep import Simulation
from pioneer import Pioneer


def main(name, environment):
    sim = Simulation(port_number=19999)
    robot = Pioneer(sim, name)
    # TODO

if __name__ == "__main__":
    parser = ArgumentParser(description="Robot control module")
    parser.add_argument("config", help="Path to environment configuration")
    parser.add_argument("name", help="Robot name")
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    main(args.name, config)
import dsdev
from dsdev import tasks
from invoke import Collection, Program

program = Program(namespace=Collection.from_module(tasks), version=dsdev.__version__)
# program.run()

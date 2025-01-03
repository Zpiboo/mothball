from cogs.movement.player import Player
from cogs.movement.context import Context
from term.commands import TermCommands
from term.utils import parse_multiline
try:
  import readline
except ModuleNotFoundError:
  print('WARNING: readline module not found.')


player = Player()
envs = []
is_dev = True
ctx = Context(player, envs, is_dev)

running = True
while running:
  try:
    cmd, sim_text = (
      parse_multiline(input(';')).strip()
        .split(' ', 1)
      + ['']*2
    )[:2]
  except KeyboardInterrupt:
    print()
    cmd, sim_text = 'exit', ''

  TermCommands.execute_command(cmd, sim_text)

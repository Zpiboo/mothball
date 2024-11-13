from cogs.movement.player import Player
from cogs.movement.context import Context
from cogs.movement.parsers import execute_string
try:
  import readline
except:
  pass

running = True
while running:
  player = Player()
  envs = []
  is_dev = True

  ctx = Context(player, envs, is_dev)

  sim_input = input(';s ')
  print()

  execute_string(ctx, sim_input)
  print(ctx.pre_out)
  print(ctx.default_string())
  print(ctx.out)

  print()
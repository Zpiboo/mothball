from copy import deepcopy
import json
import os
import sys
from cogs.movement.context import Context
from cogs.movement.player import Player
from cogs.movement.parsers import execute_string
from cogs.movement.utils import SimError


class ShellCommands:
  commands_registry = {}
  sim_history = []
  env = []
  params = {}

  with open('params.json', 'r') as input:
    params = json.load(input)


  @classmethod
  def sim(cls, context: Context, input: str) -> Context:
    execute_string(context, input)
    cls.sim_history.append(deepcopy(context.player))

    return context


  @classmethod
  def generic_sim(cls, input, history = False, *, color_output = True) -> None:
  
    context = Context(Player(), [cls.env], cls.params['is_dev'], cls.sim_history)
  
    errored = True
    try:
      cls.sim(context, input)
  
      if history:
        results = context.history_string()
      elif color_output:
        results = context.result()
      else:
        results = context.result(backup=True)
  
      errored = False
    except SimError as e:
      results = str(e)
    except:
      if cls.params['is_dev']:
        raise
      results = 'Something went wrong.'
  
    if context.macro:
      output = results + '\n' + context.macro_csv()
    else:
      output = results
  
    ##### Test this function ##################
    # if context.adding_output:                 #
    #     context.adding_output = False         #
    #     kwargs['content'] = results + "\n```" #
    ##### Test this function ##################
    print(output)


  @classmethod
  def command(cls, *, aliases=[]):
    def wrapper(cmd):
      for cmd_name in (cmd.__name__, *aliases):
        cls.commands_registry[cmd_name] = cmd
      return cmd
    return wrapper


  @classmethod
  def execute_command(cls, cmd_name: str, text: str):
    if cmd_name not in cls.commands_registry:
      print(f'Please enter a valid command ("{cmd_name}").')
      return
    cls.commands_registry[cmd_name](cls, text=text)


@ShellCommands.command(aliases=['sim', 's'])
def simulate(cls, *, text: str):
  cls.generic_sim(text)

@ShellCommands.command(aliases=['ncsim', 'ncs', 'nsim', 'ns'])
def nocolor_simulate(cls, *, text: str):
  cls.generic_sim(text, color_output=False)

@ShellCommands.command(aliases=['his', 'h'])
def history(cls, *, text: str):
  cls.generic_sim(text, history=True)

@ShellCommands.command(aliases=['clear', 'cls', 'c'])
def clearscreen(cls, **_):
  os.system('cls' if os.name == 'nt' else 'clear')

@ShellCommands.command(aliases=['x'])
def exit(cls, **_):
  print('Goodbye!')
  sys.exit(0)

# @ShellCommands.command(aliases=['t'])
# def then(cls, ctx: dict, *, text: str):
#   if 'index' not in ctx:
#     print('huh what no index???')
#     return

#   index = ctx['index']
#   cls.generic_sim(ctx, text, continuation=index)

# @ShellCommands.command(aliases=['th'])
# def thenh(cls, ctx: dict, *, text: str):
#   if 'index' not in ctx:
#     print('wtf theres no ctx!??')
#     return

#   index = ctx['index']
#   cls.generic_sim(text, continuation=index, history=True)

# @commands.Cog.listener()
# async def on_message_edit(self, before: discord.Message, after: discord.Message):
#   if after.id not in self.msg_links:
#     return

#   await self.edit_down(after.channel, after)

# async def edit_down(self, channel, msg):
#   text = msg.content
#   history = any(text.startswith(cmd) for cmd in (';history ', ';his ', ';h ', ';thenh ', ';th '))
#   for i in range(len(text)):
#     if text[i].isspace():
#       text = text[i+1:]
#       break

#   if msg.reference:
#     continuation = msg.reference.message_id
#   else:
#     continuation = None

#   await self.generic_sim(channel, text, history = history, edit = self.msg_links[msg.id], continuation = continuation)

#   for child_id in self.msg_links[msg.id].children:
#     child = await channel.fetch_message(child_id)
#     await self.edit_down(channel, child)
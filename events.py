import discord, os, pickle

from dotenv import load_dotenv
from discord.ext import commands
from splinter import Browser
from selenium.webdriver.support.ui import Select

#-----------------------------------------------------------DISCORD CONFIGURATION-----------------------------------------------------------

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=';')

#-----------------------------------------------------------SPLINTER CONFIGURATION----------------------------------------------------------

driver = Browser('chrome', headless=True)
sele_drv = driver.driver

#-----------------------------------------------------------------FUNCTIONS-----------------------------------------------------------------

def event():
  if 'Codemasters' in driver.title:
    driver.fill('Email', os.getenv('RACENET_LOGIN'))
    driver.fill('Password', os.getenv('RACENET_PASSWD') + '\n')
  sele_drv.implicitly_wait(20)
  driver.find_by_text('Create Championship').click()
  driver.select('eventCount', '3')
  driver.select('stageCount', '6')
  driver.find_by_text('Generate').click()
  sele_drv.implicitly_wait(20)
  cars = Select(sele_drv.find_element_by_id('vehicleClassRestriction')).first_selected_option.text
  f = open('cars.pckl', 'wb')
  pickle.dump(cars, f)
  f.close()
  driver.select('durationDays', '4')
  driver.find_by_xpath('//*[@class="svg-inline--fa fa-arrow-circle-right fa-w-16 fa-2x"]').click()
  driver.select('durationDays', '4')
  Select(sele_drv.find_element_by_name('vehicleClassRestriction')).select_by_visible_text(cars)
  driver.find_by_xpath('//*[@class="svg-inline--fa fa-arrow-circle-right fa-w-16 fa-2x"]').click()
  driver.select('durationDays', '4')
  Select(sele_drv.find_element_by_name('vehicleClassRestriction')).select_by_visible_text(cars)
  driver.find_by_class('btn btn-standard btn-medium ').click()
  # driver.find_by_text('Create Championship').click()
  driver.find_by_text('Advanced Settings').click()
  driver.find_by_text('Use unexpected moments').click()
  driver.find_by_text('Force cockpit camera').click()
  driver.find_by_text('Allow assists').click()
  driver.find_by_text('Submit Championship').click()

def test():
  driver.visit(os.getenv('CLUB_LINK'))
  event()
  driver.visit(os.getenv('CLUB_LINK'))

#----------------------------------------------------------------BOT COMMANDS----------------------------------------------------------------

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(print('Nie zesraj się'))
    else:
        raise error

bot.remove_command('help')
@bot.command()
async def help(ctx):
  embed = discord.Embed(title='Usage: ;command', description="", color=0xeee657)
  embed.add_field(name=';help', value='Wyświetla to okno', inline=False)
  embed.add_field(name=';dlc', value='Tworzy mistrzostwa dla "Piwnica Rally DLC"', inline=False)
  await ctx.send(ctx.message.channel, embed=embed)
    
@bot.command(name='dlc', help='Tworzy mistrzostwa dla "Piwnica Rally DLC"')
async def dlc(ctx):
  test()
  sele_drv.implicitly_wait(20)
  kraj1 = sele_drv.find_element_by_xpath('//*[@id="root"]/div/div/main/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div').text.split('\n')
  kraj2 = sele_drv.find_element_by_xpath('//*[@id="root"]/div/div/main/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div').text.split('\n')
  kraj3 = sele_drv.find_element_by_xpath('//*[@id="root"]/div/div/main/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[1]/div').text.split('\n')
  f = open('cars.pckl', 'rb')
  cars = pickle.load(f)
  f.close()
  embed = discord.Embed(title='Mistrzostwa Nowej Piwnicy w Dirt Rally 2.0', description='', color=0xff0000)
  # embed.add_field(name='', inline=True)
  embed.add_field(name='Piwnica Rally DLC:trophy:', inline=True)
  embed.add_field(name='Grupa:', value='', inline=True) # '{}'.format(cars)
  embed.add_field(name='Rajdy:', value='', inline=True) # '{}'.format(kraj1[1])
  # embed.add_field(name='', inline=True)
  embed.set_footer(text='Na każdy rajd są 4 dni. POWODZENIA!', inline=True)
  await ctx.send(ctx.message.channel, embed=embed)
  open('cars.pckl', 'w').close()
  driver.close()

bot.run(TOKEN)
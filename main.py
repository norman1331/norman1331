import discord, os
import requests, json

from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
permission_value = 8
permissions = discord.Permissions(permission_value)

token = os.environ['TOKEN']
api_key= os.environ['API']


# Event triggered when the bot is ready
@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name} ({bot.user.id})')
  print('------')

bot.remove_command('help')

@bot.command()
async def master(ctx, domain):
  await ctx.send(f'Your given master domain across all engines: !master{domain}')
  #increase threading in future where engines can handle concurrent requests
  await crawl(ctx, domain)
  await find_service(ctx, domain)

@bot.command()
async def help(ctx):
  
    embed = discord.Embed(
          title='Help menu:',
          description=' **ipaddr** -> **!ipaddr** query [For IP Lists]\n **normals** -> **!normals** query [For location search]\n **vulns** -> **!vulns** query [For vulnerability search]\n **learn** -> **!learn** [For resources to learn about shodan search]\n **protect** -> **!protect** [For resources to protection measures against shodan indexing\n [query = ip address[8.8.8.8] / domain [tesla.com] / general query any IOT device[webcam, smart watch]',
          color=discord.Color.green()
      )
    
    await ctx.send(embed=embed)



@bot.command()

async def ipaddr(ctx, ip_address):
 
  
      await ctx.send(f'Given query: !ipaddr {ip_address}')
      embed = discord.Embed(
          title='Disclaimer',
          description='This information is provided for educational and ethical purposes only. The tool author is not responsible for your actions. We suggest you use it responsibly.',
          color=discord.Color.red()
      )
      
      await ctx.send(embed=embed)
      url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={ip_address}" 
      req = requests.get(url)
      d = req.json()
      d = json.loads(req.text)
      counter = 0
    
      for x in d['matches']:
        if counter < 10:
    
          f ="IP Address:"+ x['ip_str'] + ' | ' + 'Port:' +  str(x['port']) + ' | ' +'Organisation:' + x['org']
          await ctx.send(f)
    
          counter += 1
        else:
          break
    
 

@bot.command()
async def normals(ctx, ip_address):
  
  await ctx.send(f'Given query: !normals {ip_address}')
  embed = discord.Embed(
      title='Disclaimer',
      description='This information is provided for educational and ethical purposes only. The tool author is not responsible for your actions. We suggest you use it responsibly.',
      color=discord.Color.red()
  )
  
  await ctx.send(embed=embed)
  url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={ip_address}"
  req = requests.get(url)
  d = req.json()
  d = json.loads(req.text)
  counter = 0
  for x in d['matches']:
    if counter < 3:
      location = str(x['location']['longitude'])+ "(Longitude)" + "/" + str(
        x['location']['latitude'])+ "(Latitude)" + " | " + "Country Name:"+ x['location']['country_name']
      f ="IP Address:"+ x['ip_str'] + ' | ' + 'Port:' +  str(x['port']) + ' | ' +'Organisation:' + x['org'] + "\nLocation: " + location
      await ctx.send(f)
      counter += 1
    else:
      break


@bot.command()
async def vulns(ctx, ip_address):
 
  await ctx.send(f'Given query: !vulns {ip_address}')  
  embed = discord.Embed(
      title='Disclaimer',
      description='This information is provided for educational and ethical purposes only. The tool author is not responsible for your actions. We suggest you use it responsibly.',
      color=discord.Color.red()
  )
  await ctx.send(embed=embed)
  url = f"https://exploits.shodan.io/api/search?query={ip_address}&key={api_key}"
  req = requests.get(url)
  d = req.json()
  d = json.loads(req.text)
  counter = 0

  for x in d['matches']:
    if counter < 10:

      f = str(x['source']) + ':' + str(x['_id'])
      await ctx.send(f)

      counter += 1
    else:
      break


@bot.command()
async def learn(ctx):

  # Create an embedded message
  embed = discord.Embed(title="Learning materials", color=discord.Color.blue())

  # Add a paragraph to the embedded message
  embed.description = "Here are some learning reference for awesome shodan queries"
  embed.add_field(
    name="Awesome shodan query reference:",
    value=
    "https://www.osintme.com/index.php/2021/01/16/ultimate-osint-with-shodan-100-great-shodan-queries/",
    inline=False)

  # Send the embedded message
  await ctx.send(embed=embed)


@bot.command()#creating bot command to suggest protection paths
async def protect(ctx):

  # Create an embedded message
  embed = discord.Embed(title="Protective measures",
                        color=discord.Color.blue())

  # Add a paragraph to the embedded message
  embed.description = "Here are some protective measures against open vulnerable devices"
  embed.add_field(
    name="How to find and remove your device from the Shodan IoT search engine",
    value="https://www.comparitech.com/blog/vpn-privacy/remove-device-shodan/",
    inline=False)
  embed.add_field(
    name="How to secure IoT devices and protect them from cyber attacks",
    value=
    "https://www.techtarget.com/iotagenda/post/How-to-secure-IoT-devices-and-protect-them-from-cyber-attacks",
    inline=False)
  embed.add_field(
    name="Medium Blog for 10 top security measures",
    value=
    "https://hashstudioz.medium.com/iot-security-10-tips-to-secure-the-internet-of-things-9013920f65f5",
    inline=False)

  # Send the embedded message
  await ctx.send(embed=embed)


@bot.event#creating bot event to handle bad inputs
async def on_command_error(ctx,error):
   if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Please try again.\nType !help for help menu")


bot.run(token)

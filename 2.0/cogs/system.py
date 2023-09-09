# Import main module
import discord, humanize, os, psutil, time, datetime, math

# Import secondary modules
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Group
from discord.ext.commands import GroupCog

# Import variables and standard functions from local file
from utils import *

# Create a cass for Group Commands
class System(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    system = app_commands.Group(name='system', description='Comando utilizado para verificar status do servidor do BOT')

    # Create subcommand
    @system.command(name='-m', description='Comando utilizado para verificar uso de memória do servidor do Bot.')
    async def memory(self, interaction: discord.Interaction,):
        
        # Trigger typing decorator
        async with interaction.channel.typing():

            # Gather physical and swap memory information
            virt = psutil.virtual_memory()
            swap = psutil.swap_memory()

            embed = discord.Embed(
                title='__USO DE MEMÓRIA__',
                description='',
                colour= discord.Color.teal()
            )
            embed.set_thumbnail(url='https://www.daskeyboard.com/images/applets/ram-usage/icon.png')
            embed.set_footer(text='Clone do comando "free" no Linux.')

            # Create dict with values wanted to show to user and convert to int
            fields = {
                        'total':int(virt.total),
                        'used':int(virt.used),
                        'free':int(virt.free),
                        'shared':int(getattr(virt, 'shared', 0)),
                        'buffers':int(getattr(virt, 'buffers', 0)),
                        'cache':int(getattr(virt, 'cached', 0)),
                        'swap_total':int(swap.total),
                        'swap_used':int(swap.used),
                        'swap_free':int(swap.free)
                        }
            
            # Process Embed
            embed = toEmbed(interaction, fields, embed, 'GiB')

            # Send Embed to user
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @system.command(name='-p', description='Comando utilizado para verificar a lista de processos, rodando no servidor do bot atualmente.')
    async def process_utilization(self, interaction: discord.Interaction, pid: int= None):

        # Trigger typing decorator
        async with interaction.channel.typing():

            # Declaration of list of processes
            listOfProcessNames = list()

            # Iterate over all running processes
            for proc in psutil.process_iter():

                # Get process detail as dictionary
                pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])

                # Append dict of process detail in list
                listOfProcessNames.append(pInfoDict)

            # Create Embed
            embed = discord.Embed(
                title='__LISTA DE PROCESSOS__',
                description='',
                colour=discord.Color.teal()
            )
            embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/510-5107145_user-check-list-icon-hd-png-download.png')
            embed.set_footer(text='Clone do comando "ps -aux" no Linux')

            # Iterate over list of running process and "merge" processes with same name into a new list
            newlist = list()
            for each in listOfProcessNames:
                if len(newlist) == 0: newlist.append(each)
                else:
                    for one in newlist:
                        match = False
                        if each['name'].lower() == one['name'].lower():
                            one['cpu_percent'] += each['cpu_percent']
                            match = True
                            break
                    if not match:
                        newlist.append(each)

            # Sort processes by CPU usage
            newlist = sorted(newlist, key=lambda procObj: procObj['cpu_percent'], reverse=False)

            # If pid provided, return only information from that pid
            if pid:
                for elem in newlist:
                    if pid == elem['pid']:
                        embed.description += f"cpu:\t{elem['cpu_percent']}\t|\tname:\t{elem['name']}\t|\tpid:\t{elem['pid']}\n"
                        break

            # Else, return list of processes
            else:
                for elem in newlist:
                    if len(str(embed)) < 5800 and len(embed.description) < 4000:
                        embed.description += f"cpu:\t{elem['cpu_percent']}\t|\tname:\t{elem['name']}\t|\tpid:\t{elem['pid']}\n"
                    else:
                        embed.description += '[...]\n'
                        break
            
            # Return to user
            await interaction.response.send_message(embed=embed, ephemeral=True)

    
    @system.command(name='-md', description='Comando para uma saida detalhada em relação a memória utilizada no servidor do Bot.')
    async def ps_mem(self, interaction: discord.Interaction, pid: int = None):

        # Trigger typing decorator
        async with interaction.channel.typing():

            # Call external function to get list of running process sorted by memory usage
            listOfRunningProcess = getListOfProcessSortedByMemory()

            embed_2 = discord.Embed(title = '__LISTA DE PROCESSOS POR USO DE RAM__', description = '', colour = discord.Color.teal())
            embed_2.set_thumbnail(url = 'https://docs.appian.com/suite/help/22.1/rpa-8.4/images/951644.png')
            embed_2.set_footer(text = '')

            # Iterate over list of running process and "merge" processes with same name into a new list
            memlist = list()
            for other in listOfRunningProcess:
                if len(memlist) == 0: memlist.append(other)
                else:
                    for one in memlist:
                        match = False
                        if other['name'].lower() == one['name'].lower():
                            one['rss'] += other['rss']
                            match = True
                            break
                    if not match:
                        memlist.append(other)

            # Sort processes by memory usage
            memlist = sorted(memlist, key=lambda procObj: procObj['rss'], reverse=True)
            
            # If pid provided, return only information from that pid
            if pid:
                for elem in memlist:
                    if pid == elem['pid']:
                        embed_2.description += f"cpu:\t{elem['cpu_percent']}\t|\tname:\t{elem['name']}\t|\tpid:\t{elem['pid']}\n"
                        break

            else:
                for elem in memlist:
                    if len(str(embed_2)) < 5800 and len(embed_2.description) < 4000:
                        embed_2.description += f"mem: {humanizer(elem['rss'], 'MiB')} | name: {elem['name']} | pid: {elem['pid']}\n"
                    else:
                        embed_2.description += '[...]\n'
                        break

            await interaction.response.send_message(embed=embed_2, ephemeral=True)


    @system.command(name='-id', description='Comando para apresentar informações detalhadas de um processo sendo executado no servidor do Bot.')
    async def ps_id(self, interaction: discord.Interaction, pid: int):

        # Trigger typing decorator
        async with interaction.channel.typing():

            p = psutil.Process(pid=pid)
            e = discord.Embed(
                title='__INFORMAÇÕES SOBRE PID__',
                description='',
                colour=discord.Color.teal()
            )
            e.set_thumbnail(url='https://icons.veryicon.com/png/o/miscellaneous/function-linear-icon/process-management-5.png')
            e.description = 'Informações detalhadas sobre um processo'
            
            with p.oneshot():
                e.add_field(name='**Nome do Processo**:', value=f'{p.name()}', inline=False)
                e.add_field(name=f'**Status**:', value=f'{p.status()}', inline=False)
                e.add_field(name=f'**PID**:', value=f'{p.ppid()}', inline=False)
                e.add_field(name='**Uso Cpu**:', value=f'{p.cpu_percent()}', inline=False)
                e.add_field(name=f'**Uso de memória**:', value=f'{round((p.memory_percent()), 1)}%', inline=False)
                e.add_field(name='**Data de criação**:', value=f'{datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")}', inline=False)

            await interaction.response.send_message(embed=e, ephemeral=True)


    uptime = discord.app_commands.Group(name='uptime', description='System subgroup - Uptime', parent=system)

    @uptime.command(name='-server', description='Comando utilizado para verificar o Uptime (Tempo desde o boot inicial) do servidor do Bot.')
    async def upt(self, interaction: discord.Interaction):
        
        # Trigger typing decorator
        async with interaction.channel.typing():

            # Check Bot's ping
            lat = round(self.bot.latency * 1000)

            # Uptime in hours
            uptime_in_hours = (time.time() - psutil.boot_time()) // (60 * 60)

            # Respond to user with the Bot's server uptime
            embed = discord.Embed(
                title='__UPTIME__',
                description='Tempo que o servidor está ligado',
                colour=3447003
            )
            embed.add_field(
                name='---',
                value=f':up: {uptime_in_hours} hrs'
            )
            embed.set_footer(text=f'Ping: {lat}ms - Servidor hospedado em casa!')
            embed.set_thumbnail(url='https://www.inconsdb.com/icons/preview/white/time-4-xxl.png')

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @uptime.command(name='-bot', description='Comando utilizado para verificar o Uptime (Tempo desde o kick off) do Bot')
    async def ubot(self, interaction: discord.Interaction):

        # Trigger typing decorator
        async with interaction.channel.typing():

            # Initialize variables:
            PROCNAME = "python.exe"
            pid = None

            # Search for PROCNAME process in running processes and assign PID to variable
            for proc in psutil.process_iter():
                if PROCNAME in proc.name().lower():
                    pid = proc.pid
                    break

            # Extract process information using psutil
            p = psutil.Process(pid)

            # Track process creation time in seconds
            p_time = p.create_time()

            # Track current time in seconds
            now = time.time()

            # Calculate difference between current time and process creation time (in seconds, minutes, hours and days)
            diff_s = math.floor(now - p_time)
            diff_m = math.floor(diff_s / 60)
            diff_h = math.floor(diff_m / 60)
            diff_d = math.floor(diff_h / 24)

            # Reply with Bot's uptime
            embed = discord.Embed(
                title='__UPTIME DO BOT__',
                description='Tempo que o Bot está ligado',
                colour=3447003
            )
            embed.add_field(name = 'Dias:', value = diff_d, inline = False)
            embed.add_field(name = 'Horas:', value = diff_h, inline = False)
            embed.add_field(name = 'Minutos:', value = diff_m, inline = False)
            embed.add_field(name = 'Segundos:', value = diff_s, inline = False)
            embed.set_thumbnail(url = 'https://www.iconsdb.com/icons/preview/white/time-4-xxl.png')

            embed.set_footer(text = f'Data de criação do processo "{PROCNAME}": {datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")}')
            
            await interaction.response.send_message(embed=embed, ephemeral=True)


def toEmbed(interaction, fields, embed, d_unit):
    for field in fields:
        embed.add_field(name = field, value = humanizer(fields[f"{field}"], d_unit))
    return embed

def getListOfProcessSortedByMemory():

    '''
    Get list of running process sorted by Memory Usage
    '''

    listOfProcObjects = []

    # Iterate over the list
    for proc in psutil.process_iter():
        try:

            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['rss'] = proc.memory_info().rss

            # Append dict to list
            listOfProcObjects.append(pinfo);
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['rss'], reverse=True)
    return listOfProcObjects

async def setup(bot):
    await bot.add_cog(System(bot))

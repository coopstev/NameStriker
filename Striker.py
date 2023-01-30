import discord
import re

# IF YOU WANT TO MODIFY THE NAMING POLICY ENFORCED, DO THAT IN THE BELOW LINE:
VALID_NAME = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð'-]+ [a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð '-]+$")

TOKEN = # TODO: ADD YOUR BOT'S TOKEN HERE
SERVER_ID = # TODO: ADD YOUR SERVER'S ID HERE
SERVER_STRIKES_CHANNEL_ID = # TODO: ADD YOU SERVER'S #strikes CHANNEL ID HERE
SERVER_NAME = # TODO: ADD YOUR SERVER'S NAME HERE

def get_invalid_name(member):
    if has_valid_name(member) : exit(0)
    if (member.nick == None):
        return member.name
    else :
        return member.nick

def has_valid_name(member):
    # TODO: If you want to make exceptions to the naming policy, do that here like I did for Dyno, a common Discord bot
    if member.name == "Dyno" : return True
    if (member.nick == None):
        return bool(VALID_NAME.fullmatch(member.name))
    else :
        return bool(VALID_NAME.fullmatch(member.nick))

def get_ids_from_list(filename):
    file = open(filename, 'r')
    liststr = file.readline()
    ids = []
    if liststr != '':
        ids = list(map(int, liststr.split(',')))
    file.close()
    return ids

def save_list(lst, filename):
    file = open(filename, 'w')
    for i in range(len(lst)):
        file.write(str(lst[i]))
        if i != len(lst) - 1 : file.write(',')
    file.close()
    return
intents = discord.Intents.default()
intents.members = True
intents.bans = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    await client.wait_until_ready()

    server = client.get_guild(SERVER_ID)
    print("members found: " + str(len(server.members)))

    striked = get_ids_from_list("striked.txt")
    strikes_channel = server.get_channel(SERVER_STRIKES_CHANNEL_ID)

    banned = get_ids_from_list("banned.txt")
    for member in server.members:
        print(f'{member.name}, nickname {member.nick}, ID {member.id}')
        if not has_valid_name(member):
            invalid_name = get_invalid_name(member)
            id = member.id
            if id in striked: # this is the second strike
                await member.send(f'"{invalid_name}" does not comply with the naming policy in the {SERVER_NAME} server. You already had one strike. Hence, you have been Banned. You will not be permitted to rejoin.')
                striked.remove(id)
                banned.append(id)
                await server.ban(member, reason=f'"{invalid_name}" does not comply with the naming policy, already had one strike')
                note = f'{member.name}, nickname {member.nick}, ID {id} received their SECOND strike for "{invalid_name}" failing to comply with the naming policy. They have been Banned and notified.'
                print(note)
                await strikes_channel.send(note)
            else : # this is the first strike
                await member.send(f'"{invalid_name}" does not comply with the naming policy in the {SERVER_NAME} server. This is your one and only strike. You have been Kicked, but you may rejoin. Please review the rules again before proceeding.')
                striked.append(id)
                await server.kick(member, reason=f'"{invalid_name}" does not comply with the naming policy, this is their first strike')
                note = f'{member.name}, nickname {member.nick}, ID {id} received their FIRST strike for "{invalid_name}" failing to comply with the naming policy. They have been Kicked and DMed a warning.'
                print(note)
                await strikes_channel.send(note)
    # now to save the updated striked/banned lists
    save_list(striked, "striked.txt")
    save_list(banned, "banned.txt")
    print("Done processing strikes.")
    return

client.run(TOKEN)
exit()

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio

async def login_and_save(api_id, api_hash, phone_number):
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)
    # You can save the session here if needed
    return client

async def scrape_usernames(client, group_username):
    group_entity = await client.get_entity(group_username)
    participants = await client(GetParticipantsRequest(
        group_entity,
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=100,
        hash=0
    ))
    usernames = []
    for user in participants.users:
        if user.username:
            usernames.append(user.username)
    return usernames

async def add_to_group(client, target_group_username, usernames):
    target_entity = await client.get_entity(target_group_username)
    for username in usernames:
        try:
            await client(InviteToChannelRequest(target_entity, [username]))
        except Exception as e:
            print(f"Failed to add {username} to the group: {e}")

async def main():
    # Your Telegram API credentials
    api_id = '15460762'
    api_hash = '9e2dba9192c637cbe850b3207f067f9e'
    phone_number = '+17023234926'

    # Login and save the session
    client = await login_and_save(api_id, api_hash, phone_number)

    # Group to scrape usernames from
    group_username = 'Arslan_MD'

    # Scrape usernames from the group
    scraped_usernames = await scrape_usernames(client, group_username)

    # Group to add scraped usernames to
    target_group_username = 'Random'

    # Add scraped usernames to the target group
    await add_to_group(client, target_group_username, scraped_usernames)

    await client.disconnect()

asyncio.run(main())

//tool made by codeprofessor

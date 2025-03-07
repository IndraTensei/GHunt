from gkia import globals as gb
from gkia.helpers.utils import get_httpx_client
from gkia.objects.base import gkiaCreds
from gkia.apis.peoplepa import PeoplePaHttp
from gkia.apis.vision import VisionHttp
from gkia.helpers import gmaps, playgames, auth, calendar as gcalendar, ia
from gkia.helpers.knowledge import get_user_type_definition

import httpx

from typing import *


async def hunt(as_client: httpx.AsyncClient, email_address: str, json_file: bool=None):
    if not as_client:
        as_client = get_httpx_client()
 
    gkia_creds = gkiaCreds()
    gkia_creds.load_creds()

    if not gkia_creds.are_creds_loaded():
        exit("[-] Creds aren't loaded. Are you logged in ?")

    if not auth.check_cookies(gkia_creds.cookies):
        exit("[-] Seems like the cookies are invalid. Exiting...")

    #gb.rc.print("[+] Target found !", style="sea_green3")

    people_pa = PeoplePaHttp(gkia_creds)
    vision_api = VisionHttp(gkia_creds)
    is_found, target = await people_pa.people_lookup(as_client, email_address, params_template="max_details")
    if not is_found:
        exit("\n[-] The target wasn't found.")

    if json_file:
        json_results = {}

    containers = target.sourceIds

    if len(containers) > 1 or not "PROFILE" in containers:
        print("\n[!] You have this person in these containers :")
        for container in containers:
            print(f"- {container.title()}")

    if not "PROFILE" in containers:
        exit("[-] Given information does not match a public Google Account.")

    container = "PROFILE"
    
    gb.rc.print("\n🙋 Google Account data\n", style="plum2")

    if container in target.names:
        print(f"Name : {target.names[container].fullname}\n")

    if container in target.profilePhotos:
        if target.profilePhotos[container].isDefault:
            print("[-] Default profile picture")
        else:
            print("[+] Custom profile picture !")
            print(f"=> {target.profilePhotos[container].url}")
            
            await ia.detect_face(vision_api, as_client, target.profilePhotos[container].url)
            print()

    if container in target.coverPhotos:
        if target.coverPhotos[container].isDefault:
            print("[-] Default cover picture\n")
        else:
            print("[+] Custom cover picture !")
            print(f"=> {target.coverPhotos[container].url}")

            await ia.detect_face(vision_api, as_client, target.coverPhotos[container].url)
            print()

    print(f"Last profile edit : {target.sourceIds[container].lastUpdated.strftime('%Y/%m/%d %H:%M:%S (UTC)')}\n")
    
    if container in target.emails:
        print(f"Email : {target.emails[container].value}")
    else:
        print(f"Email : {email_address}\n")

    print(f"Gaia ID : {target.personId}")

    if container in target.profileInfos:
        print("\nUser types :")
        for user_type in target.profileInfos[container].userTypes:
            definition = get_user_type_definition(user_type)
            gb.rc.print(f"- {user_type} [italic]({definition})[/italic]")

    gb.rc.print(f"\n📞 Google Chat Extended Data\n", style="light_salmon3")

    #print(f"Presence : {target.extendedData.dynamiteData.presence}")
    print(f"Entity Type : {target.extendedData.dynamiteData.entityType}")
    #print(f"DND State : {target.extendedData.dynamiteData.dndState}")
    gb.rc.print(f"Customer ID : {x if (x := target.extendedData.dynamiteData.customerId) else '[italic]Not found.[/italic]'}")

    gb.rc.print(f"\n🌐 Google Plus Extended Data\n", style="cyan")

    print(f"Entreprise User : {target.extendedData.gplusData.isEntrepriseUser}")
    #print(f"Content Restriction : {target.extendedData.gplusData.contentRestriction}")
    
    if container in target.inAppReachability:
        print("\n[+] Activated Google services :")
        for app in target.inAppReachability[container].apps:
            print(f"- {app}")

    gb.rc.print("\n🎮 Play Games data", style="deep_pink2")

    player_results = await playgames.search_player(gkia_creds, as_client, email_address)
    if player_results:
        player_candidate = player_results[0]
        print("\n[+] Found player profile !")
        print(f"\nUsername : {player_candidate.name}")
        print(f"Player ID : {player_candidate.id}")
        print(f"Avatar : {player_candidate.avatar_url}")
        _, player = await playgames.get_player(gkia_creds, as_client, player_candidate.id)
        playgames.output(player)
    else:
        print("\n[-] No player profile found.")

    gb.rc.print("\n🗺️ Maps data", style="green4")

    err, stats, reviews, photos = await gmaps.get_reviews(as_client, target.personId)
    gmaps.output(err, stats, reviews, photos, target.personId)

    gb.rc.print("\n🗓️ Calendar data\n", style="slate_blue3")

    cal_found, calendar, calendar_events = await gcalendar.fetch_all(gkia_creds, as_client, email_address)

    if cal_found:
        print("[+] Public Google Calendar found !\n")
        if calendar_events.items:
            if "PROFILE" in target.names:
                gcalendar.out(calendar, calendar_events, email_address, target.names[container].fullname)
            else:
                gcalendar.out(calendar, calendar_events, email_address)
        else:
            print("=> No recent events found.")
    else:
        print("[-] No public Google Calendar.")

    if json_file:
        if container == "PROFILE":
            json_results[f"{container}_CONTAINER"] = {
                "profile": target,
                "play_games": player if player_results else None,
                "maps": {
                    "photos": photos,
                    "reviews": reviews,
                    "stats": stats
                },
                "calendar": {
                    "details": calendar,
                    "events": calendar_events
                } if cal_found else None
            }
        else:
            json_results[f"{container}_CONTAINER"] = {
                "profile": target
            }

    if json_file:
        import json
        from gkia.objects.encoders import gkiaEncoder;
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_results, cls=gkiaEncoder, indent=4))
        gb.rc.print(f"\n[+] JSON output wrote to {json_file} !", style="italic")

    await as_client.aclose()
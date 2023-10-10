from gkia.knowledge.services import services_baseurls
from gkia.knowledge.keys import keys
from gkia.knowledge.maps import types_translations
from gkia.knowledge.people import user_types
from gkia.knowledge.sig import sigs
from gkia.errors import gkiaKnowledgeError

from typing import *


def get_domain_of_service(service: str) -> str:
    if service not in services_baseurls:
        raise gkiaKnowledgeError(f'The service "{service}" has not been found in gkia\'s services knowledge.')
    return services_baseurls.get(service)

def get_origin_of_key(key_name: str) -> str:
    if key_name not in keys:
        raise gkiaKnowledgeError(f'The key "{key_name}" has not been found in gkia\'s API keys knowledge.')
    return keys.get(key_name, {}).get("origin")

def get_api_key(key_name: str) -> str:
    if key_name not in keys:
        raise gkiaKnowledgeError(f'The key "{key_name}" has not been found in gkia\'s API keys knowledge.')
    return keys.get(key_name, {}).get("key")

def get_gmaps_type_translation(type_name: str) -> str:
    if type_name not in types_translations:
        raise gkiaKnowledgeError(f'The gmaps type "{type_name}" has not been found in gkia\'s knowledge.\nPlease open an issue on the gkia Github or submit a PR to add it !')
    return types_translations.get(type_name)

def get_user_type_definition(type_name: str) -> str:
    if type_name not in user_types:
        raise gkiaKnowledgeError(f'The user type "{type_name}" has not been found in gkia\'s knowledge.\nPlease open an issue on the gkia Github or submit a PR to add it !')
    return user_types.get(type_name)

def get_package_sig(package_name: str) -> str:
    if package_name not in sigs:
        raise gkiaKnowledgeError(f'The package name "{package_name}" has not been found in gkia\'s SIGs knowledge.')
    return sigs.get(package_name)
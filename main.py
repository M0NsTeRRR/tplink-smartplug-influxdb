# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
#
# Ce logiciel, tplink-smartplug-influxdb, est un programme informatique servant à
# remonter les informations de smartplugs TP-Link à influxdb.
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import logging
from os import environ as os_environ
from json import load as json_load
from sys import exit as sys_exit
from ipaddress import IPv4Address as ipaddressIPv4
from requests import post as requests_post
from time import sleep as time_sleep

from tplink_smartplug import SmartPlug


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

config = {}  # configuration
smartplugs = []  # list of smartplug objects
# get configuration from file or env
try:
    with open('config.json') as json_data_file:
        config.update(json_load(json_data_file))
        config["nb_smartplug"] = len(config["smartplugs"])
except FileNotFoundError:
    # if file not found get env values
    config = {
        "influxdb": {
            "url":  os_environ.get("INFLUXDB_URL", ""),
            "database": os_environ.get("INFLUXDB_DATABASE", ""),
            "username": os_environ.get("INFLUXDB_USERNAME", ""),
            "password": os_environ.get("INFLUXDB_PASSWORD", "")
        },
        "delay": int(os_environ.get("DELAY", 0)),
        "nb_smartplug": int(os_environ.get("NB_SMARTPLUG", 0)),
        "smartplugs": []
    }

    for i in range(0, config["nb_smartplug"]):
        name_smartplug = "SMARTPLUG_" + str(config["nb_smartplug"])
        config["smartplugs"].append(os_environ.get(name_smartplug, ""))
except Exception as error:
    sys_exit(f'{error}')

# check configuration
try:
    if not config["influxdb"]["url"]:
        raise Exception(f"INFLUXDB_URL can't be empty, value={config['influxdb']['url']}")
    if not config["influxdb"]["database"]:
        raise Exception(f"INFLUXDB_DATABASE can't be empty, value={config['influxdb']['database']}")
    if not config["influxdb"]["username"]:
        raise Exception(f"INFLUXDB_USERNAME can't be empty, value={config['influxdb']['username']}")
    if not config["influxdb"]["password"]:
        raise Exception(f"INFLUXDB_PASSWORD can't be empty, value={config['influxdb']['password']}")
    if config["delay"] < 10 or config["delay"] > 3600:
        raise Exception(f"DELAY must be in range [10, 3600], value={config['delay']}")
    if config["nb_smartplug"] < 1:
        raise Exception(f"NB_SMARTPLUG must be superior or equal to 1, value={config['nb_smartplug']}")
except Exception as error:
    sys_exit(f'{error}')

for i in range(0, config["nb_smartplug"]):
    ip_smartplug = str(ipaddressIPv4(config["smartplugs"][i]))
    smartplugs.append(SmartPlug(ip_smartplug))

while True:
    try:
        data = ""
        for smartplug in smartplugs:
            data += "hs110,"
            smartplug_data = smartplug.info
            smartplug_data.update(smartplug.emeter_stats())
            data += f'hs110 mac="{smartplug_data["mac"]}",version="{smartplug_data["sw_ver"]}",name="{smartplug_data["alias"]}",state={smartplug_data["relay_state"]},voltage_mv={smartplug_data["voltage_mv"]},current_ma={smartplug_data["current_ma"]},power_mw={smartplug_data["power_mw"]},total_wh={smartplug_data["total_wh"]}\n'

        r = requests_post(config["influxdb"]["url"] + '/write', data=data, params={'db': config["influxdb"]["database"], 'u': config["influxdb"]["username"], 'p': config["influxdb"]["password"]})
        if r.status_code != 204:
            logger.error(f'Error can\'t send data to InfluxDB URL --> {config["influxdb"]["url"]}\nHTTP Error code --> {r.status_code}')
        else:
            logger.info(f'{data}')
    except Exception as error:
        logger.error(f'{error}')

    time_sleep(config["delay"])

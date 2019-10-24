[![Codacy Badge](https://api.codacy.com/project/badge/Grade/975f9c9d85ce4fb1b4c7f56a0735566e)](https://www.codacy.com/manual/M0NsTeRRR/tplink-smartplug-influxdb?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=M0NsTeRRR/tplink-smartplug-influxdb&amp;utm_campaign=Badge_Grade)
[![Docker Automated build](https://img.shields.io/docker/cloud/automated/monsterrr/tplink-smartplug-influxdb?style=flat-square)](https://hub.docker.com/r/monsterrr/tplink-smartplug-influxdb)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/monsterrr/tplink-smartplug-influxdb?style=flat-square)](https://hub.docker.com/r/monsterrr/tplink-smartplug-influxdb)

The goal of this project is to get data of tplink-smartplugs and to send data to an influx database. 

## Requirements
#### Classic
- Python >= 3.7
- Pip3

#### Docker
- Docker CE

## Install
### Classic
Install the requirements `pip install -r requirements.txt`

Fill config.json with some informations :

- Delay can be must be set in range [10,3600]
```json
{
  "influxdb": {
      "url": "http://influxdb.com/",
      "database": "tplinkplug",
      "username": "username",
      "password": "password"
  },
  "delay": 60,
  "smartplugs": [
    "192.168.0.1",
    "192.168.0.2",
    "192.168.0.3"
  ]
}
```
Start the script `python main.py`

### Docker
Fill environment variables
`SMARTPLUG_X=` replace X with the number of your smartplug

`docker run -d --restart=always -e "INFLUXDB_URL=" -e "INFLUXDB_DATABASE=" -e "INFLUXDB_USERNAME=" -e "INFLUXDB_PASSWORD=" -e "DELAY=" -e "NB_SMARTPLUG=" -e "SMARTPLUG_X=" monsterrr/dealabs-price-error:latest`

Example :

`docker run -d --restart=always -e "INFLUXDB_URL=http://influxdb.com/" -e "INFLUXDB_DATABASE=tplinkplug" -e "INFLUXDB_USERNAME=username" -e "INFLUXDB_PASSWORD=password" -e "DELAY=60" -e "NB_SMARTPLUG=2" -e "SMARTPLUG_1=192.168.0.1" -e "SMARTPLUG_2=192.168.0.2" monsterrr/dealabs-price-error:latest`
# Licence

The code is under CeCILL license.

You can find all details here: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - mastership@hotmail.fr

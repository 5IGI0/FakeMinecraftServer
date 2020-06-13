# Fake Minecraft server

The purpose of this script is to create a fake Minecraft server.

![example](./assets/server.png)

## configuration files

### config.json

key         | description                                 | example
-           | -                                           | -
port        | the binding port                            | 25565
player_slot | number of player slots                      | 90000
rush_hour   | number of players in rush hour              | 60000
min_player  | minimum number of players connected         | 25000
random      | maximum of random value in number of player | 10000

### kick_payload.json
- The payload sent when a player tries to connect to the server
### status_payload.json
- The payload sent when Minecraft fetches the server status
### favicon.png
- The icon of the server !! **the logo has to be 64x64** !!

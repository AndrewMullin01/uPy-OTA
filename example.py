import machine

####################################################################
# Wifi
####################################################################
import wifi

wifi.connect() # Can't update from Github without a network connection...

####################################################################
# OTA Github updates
####################################################################

import ota

updater = ota.OTA(
    user="SeymoreButtz",
    repo="super-cool-project",
    branch="main",
    access_token  = "github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)
  
did_update = updater.update()
if did_update:
  machine.reset()
    

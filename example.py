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

print("Checking for updates...")
files_updated = updater.update()

print(f"Done. {files_updated} files updated.")
if files_updated > 0:
  print("Resetting...")
  machine.reset()
    

# Kek that didn't last long
# Someone else has already made a decent BLE cli implement for BlueZ (albeit in Rust, but everybody has their issues 😝), which this was a stepping stone to doing. Makes my life easier since I just need to write a python wrapper (I forget cli args with all the RF stuff I have done and vastly prefer prompts). Check it out here https://github.com/elijah629/flipper-rpc

# pyQFlipper
CLI Menu based Serial python implementation of Flipper CLI api to enable file transfer (both to and from the Flipper), as well as rename and deletion of files on the Flipper.

This is likely not useful to many, as Qflipper, the Android App, and Flipper Lab cover most use cases.
Unfortunately I use a linux phone (with an Android container) which doesn't have bluetooth passthrough so the Android App doesn't work for me.
Qflipper does work and installs/Sees the flipper just fine.....But phosh does not support drag and drop.
Web Serial would probably also work, but I didn't want to install Chromium solely for that purpose, and also want offline functionality. 

So I built this to transfer files back and forth with a USB-C.

I had originally planned to incorporate Update functionality, but I am not far enough along in understanding the flipper RPC communication.

pyFlipper Repo: https://github.com/wh00hw/pyFlipper/ 
was referenced once or twice, but ultimately discarded with my own implements built.

PyFlipper is a straight implement of the Flipper CLI API. pyQFlipper provides a user menu, and abuses the Flipper CLI API to upload and download instead of just moving things internally on the flipper. I also found PyFlipper to be a bit overkill.

Most of my testing was doing using Subghz files. If you see a bug please let me know

# Usage:
- Install the python Serial package according to your distro. Ensure group/user permissions are set appropriately.
- Grant qflippercli.py execute permission.
- Run it (should work from any folder/path)
  - Upload files need to be in the same directory as qflippercli.py
  - Similarly, downloaded files can be found in that same directory
- One operation is done each time (One Upload/Download/Rename/Deletion) then it cycles back to the Main Menu ready for another operation.
- Filenames can but don't need to include the file extension.
  - I take the user input as a search term for files in that directory
  - There are file checks on both the Flipper and Locally. The operation is aborted if there is a conflict (eg trying to download Garage.sub if there is already a Garage.sub locally. Same for Uploads/Rename/Deletion if the files already exist/or if the desired file cannot be found due to a typo)

# License:
You are free to use this for any purpose you desire provided attribution is provided or Splash Screen is retained

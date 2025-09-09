# pyQFlipper
CLI Menu based Serial python implementation of Flipper CLI api to enable file transfer (both to and from), as well as rename and deletion

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

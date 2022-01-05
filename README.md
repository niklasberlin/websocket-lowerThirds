# Tornado based Webserver for Lower Thirds

# do not consider this stable! althoug it worked well for a four day conference

This is a websocket example for lower Thirds written in python. It is intended to be used by the xHain Hack and Makespace in Berlin during the second edition of the remote chaos experience (rc3 rev2) from the CCC in 2021.

## Installation

1. `pip install -r requirements.txt`

2. `python app.py`

3. http://localhost:8888/

4. Send a REST call:

## REST API examples

Set the first line ot the lower Third to "lineone" and the second line to "linetwo", the lower third will be displayed for 4000ms:
- `curl "http://localhost:8888/api?l1=lineone&l2=linetwo&d=4000"`

## Webinterface

there are two webinterfaces available for controlling the lower Thirds:

http://localhost:8888/control.html

and 

http://localhost:8888/control-vue.html

the first one can be considered deprecated and will probably be removed in the future

## customizing Lower Thrids

The lower thirds are created as a html/css webpage, the default javascript code just handles the websocket connection and will add a "visible" class to the element with the id="lower-third-container". All Animations are handled by CSS. Use index-new.html and style.css as an exmaple

if you want to use multiple designs at the same time you can open them just by calling the appropiate URL, for example: http://localhost:8888/index-new.html

the Default Design is set in the  "IndexHandler" function in app.py

## import Fahrplan

if the event is planned using pretalx a Fahrplan/shedule can be imported to create lower Thrids for all registred speakers

## OBS integration

This tool can also be used to set a Text-source in OBS, just configure the Settings at the beginning of the script (IP, Port, Password, Source-Name)

## Companion integration

it is possible to trigger actions in companion (for example showing the text-source in OBS with some other timed actions (background graphics, ...)
you can define a page and button to virtually press on the "show" action and another page/button combination that will be triggert with the "hide" action

in Companion the OSC control need to be activated in the settings

## License
This script is licenced unter the MIT Licence

the required librarys are licenced as followed:
|library|licence|link|
|---|---|---|
|python-osc | The Unlicense | https://github.com/attwad/python-osc |
|obs-websocket-py | MIT License | https://github.com/Elektordi/obs-websocket-py |
|tornado | Apache License 2.0 | https://github.com/tornadoweb/tornado |
|requests | Apache License 2.0 | https://github.com/psf/requests |
|pydantic | MIT License | https://github.com/samuelcolvin/pydantic |


[![Build Status](https://travis-ci.org/ibtehaz-shawon/zathura.svg?branch=master)](https://travis-ci.org/ibtehaz-shawon/zathura)

```
______       ___________                       
___  /______ __  /___  /_____  ______________ _
__  / _  __ `/  __/_  __ \  / / /_  ___/  __ `/
_  /__/ /_/ // /_ _  / / / /_/ /_  /   / /_/ / 
/____/\__,_/ \__/ /_/ /_/\__,_/ /_/    \__,_/  
```
# Zathura
Zathura is a sqlite3 based logger. Currently, you can see your error and debug logs from terminal only. However, I am working on webview. Do keep in mind, you will have to handle the authentication for your own project.

-------------------------------
## How to install
<ul> <pre> pip install zathura </pre> </ul>
This will install the latest version on your virtualenv

-------------------------------
## Code Preview
<p>
1.  You can just import Zathura from ZathuraProject.zathura and call insert_error_log function to start logging your errors right away.
<pre>
from ZathuraProject.zathura import Zathura

zathura = Zathura()
zathura.insert_error_log(user_id, error_name, long_error_description)
</pre>
</p>

<p>
2. View your logs from terminal
<pre>
zathura help
</pre>
This will list all the avaiable command for you. Choose from them to see how you want to sort your logs.
<pre>
usage: Zathura COMMAND [args] ...
For example: { Zathura v } will show the current version of this pacakge.
-----------------------------------------------------
-----------------------------------------------------
All commands: 
[[ v ]] : Show the current version of this package
[[ developer ]] : Search based on developers name. You can filter out the result based on date and descending order
[[ debug_origin ]] : Shows debug messages based on point of origin. Point of origin is the class/function from where you are adding a message in sqlite.
[[ error_user ]] : Shows error generated under the given username
[[ all_debug ]] : Shows all debug messages
[[ error_name ]] : Shows error based on a error name.
[[ date ]] : Shows error occurred in between a specific date.
[[ all_error ]] : Shows all error messages
[[ origin ]] : Shows error generated on the given point of origin
[[ mark_resolve ]] : Given an error name and point of origin all errors logged on database, is marked resolved.
[[ delete_debug ]] : Deletes the last seven days of debug mesasges from the database. It is useful if you dont want to clutter the database with unnecessary debug info.
[[ help ]] : Shows all the commands necessary to run this package from terminal
-----------------------------------------------------
-----------------------------------------------------
</pre>
For example to see all error, without sorting you can just type
<pre> zathura all_error </pre>
</p>

-------------------------------

<h3> 
It is without doubt that there might be some bugs and improvement for this project. I wrote zathura to help me with my projects. If you face any bugs or want some more modules, please open an issue. If you want to contribute, please clone my project and create a pull request for me. 
</h3>

<p> Thank you. Ibtehaz </p>

-------------------------------

## Run Zathura codebase on your computer
<ol>

<li>
Clone the project and change your directory into it.
</li>

<li>
    pip install -r requirements.txt
</li> <li>
    pip install --upgrade setuptools wheel
</li> <li>
    python3 setup.py sdist bdist_wheel
    <br>
    This will create a build file for you from the laterst version.
</li> <li>
    pip install . <br>
    To check on your machine
</li>
</ol>

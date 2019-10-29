[![Build Status](https://travis-ci.org/p1r-a-t3/zathura.svg?branch=master)](https://travis-ci.org/p1r-a-t3/zathura)

```
______       ___________
___  /______ __  /___  /_____  ______________ _
__  / _  __ `/  __/_  __ \  / / /_  ___/  __ `/
_  /__/ /_/ // /_ _  / / / /_/ /_  /   / /_/ /
/____/\__,_/ \__/ /_/ /_/\__,_/ /_/    \__,_/
```

# Zathura

Zathura is a utility package for Bugtracker (<https://github.com/p1r-a-t3/Bugtracker).> Currently, zathura can send error and verbose logs from projects. Future features include parsing `nohup.out` file to check probably logs/errors etc.

---

## How to install

`pip install zathura`

This will install the latest version on your virtualenv

---

## Code Preview

Zathura works with bugtracker. So, You already have a project access token from the bugtracker. It's like 'API Key' to uniquely identify a project.

Here is a simple code snippet to initiate the class and start logging away

```
from ZathuraProject.zathura import Zathura
zathura = Zathura(bugtracker_url="Your_Bugtracker_URL_HERE",
                  project_token="Your_Project_Token_HERE")


# Logging Error logs.
zathura.send_error_log_bugtracker("An Error name", "A good error description", user = "username")

# Logging verbose Logs
zathura.send_verbose_log_bugtracker("Verbose description", user = "username")
```

user is an optional field in both case. That's it, you just logged an error and a debug message on your server. 

---

With <3 from p1r-a-t3

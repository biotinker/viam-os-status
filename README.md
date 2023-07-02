# osstats modular sensor component

*osstats* is a Viam modular sensor component that provides a variety of operating system feedback for unix systems

## API

The osstats resource fulfills the Viam sensor and generic interfaces

### get_readings()

The *get_readings()* command takes no arguments, and returns the stdout and stderr results of running the configured commands.

By default the following commands are run:

```
uptime
iwconfig
df -h
```

## Viam Component Configuration

The module should be added as so:
``` json
  "modules": [
    {
      "name": "osstats",
      "executable_path": "/path/to/viam-os-status/run.sh"
    }
  ]
```

This component should be configured as type *sensor*, model *biotinker:sensor:osstats*.

Two config options are supported.

First, `ext_cmds_allowed` (default False) which if set to `True` allows arbitrary commands to be run via `Do`

Second, `commands` (default empty list) which is a list of additional command executable and arguments to be run. The contents of each of these lists will be run directly as the main argument of `subprocess.run()`

Example:

``` json
  "components": [
    {
      "name": "os",
      "type": "sensor",
      "model": "biotinker:sensor:osstats",
      "attributes": {
        "commands": [
          ["ls", "-l"]
        ]
      },
      "depends_on": []
    }
  ]
```

If external commands are enabled with 
``` json
      "attributes": {
        "ext_cmds_allowed": "true"
      }
```

Then the Do command may be used to run any arbitrary command as follows:
```
    osstats = Sensor.from_robot(robot, "name of your osstats sensor")
    result = await os.do_command({"run":["ls", "-l"]})
    print(result)
```

All commands will return with one of two possibilities:

1) Two fields, labeled `stdout` and `stderr`, with the contents of each from running the command, or

2) One field, labeled "error", which will be returned if the running of the command threw an exception (for example if the executable does not exit). The field contains the contents of the exception.

*Note:* the python `subprocess` module requires arguments to be specified separately. `["ls myfile"]` will throw an error, while `["ls", "myfile"]` will return the desired result.

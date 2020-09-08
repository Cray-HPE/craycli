NWMGMT-2139

`craycli` allows for a "remote swagger", to specify the swagger file based on
the committed stash URL as specified in a `.remote` file.  Unfortunately,
the `slingshot_msgapi/specs/api/controller/fabric_v2.yaml` is a "referential"
swagger that refers to components in other files.

Therefore we needed to use a post-processed swagger file that already transcluded
all its dependencies.  Fortunately one was already pre-made via 
[fabric-controller/fms/swagger/api/swagger.yaml](https://stash.us.cray.com/projects/NWMGMT/repos/fabric-controller/browse/fms/swagger/api/swagger.yaml).

Using this as reference (and mucking with the `servers` field), we were 
able to pull the `fabric_v2` swagger into `craycli`.

```
    "servers": [
        {
            "url": "http://fms-fc:8081/apis/fc/v2"
        }
    ],
```


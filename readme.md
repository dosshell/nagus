# Nagus

Nagus is simple and generic package manager. It is designed to integrate well with your building
toolchain, for example cmake. The benefit with Nagus compared to git-lfs and nuget is that you only
need one copy of the packages stored localy, no matter what how many clones you have. To create a
package you make a zip file and upload it to a server. The name of the zip file will be the package
name. Therefor we recommend that you use to use a version naming scheme like: package-1.2.3.zip or
similar.

## Get Started
- Install Nagus
- Run `nagus stash ~/my_nagus_stash`
- Creeate an empty text document and create a zip file of it named `my_package-1.0.0.zip`
- Copy the zip file to a server
- Add a `nagus_packages.json` in you git repo with following information:
```
{
    "packages": [
        "my_package-1.0.0"
    ],
    "servers": [
        "/your/path/to/the/server/directory/"
    ]
}
```
- You can now run `nagus add nagus_packages.json` and it will download the missing packages to your
stash.


## More Examples

### Command Line
```
nagus add package_name-2.7.3 another_packge-1.0.2
nagus add nagus_packages.json

nagus add user:password@\\smbserver\share\folder\but\this\will\only\work\in\windows
nagus add /folder/something/
nagus add //server/share/folder/
nagus add c:\folder\

nagus rm package_name-2.7.3 another_package-1.0.2
nagus rm /folder/something/
nagus rm c:\folder\
nagus rm *

nagus keep ../
nagus keep python-2.7.3 opencv-1.2.3
nagus keep nagus_packages.json

nagus view servers
nagus view packages
nagus view nagus.json

nagus stash c:\nagus_stash\
```

### Cmake Integration
```
add_custom_command(TARGET ${PROJECT_NAME}
    PRE_BUILD
    COMMAND nagus add nagus_packages.json
)
```

### More Json Examples
```
{
    "packages": [
        "somepackage-1.3.7",
        "anotherpackage-5.0.10"
    ],
    "servers": [
        "user:password@\\\\smbserver\\share\\folder\\",
        "/some/mounted/slow/NFS/drive/"
	]
}
```
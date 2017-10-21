# Nagus

usage:
```
nagus add package_name-2.7.3 another_packge-1.0.2
nagus add nagus_packages.json

nagus add user:password@\\smbserver\share\folder\
nagus add /folder/something/
nagus add c:\folder\

nagus rm package_name-2.7.3 another_package-1.0.2
nagus rm /folder/something/
nagus rm c:\folder\
nagus rm *

nagus keep ../
nagus keep python-2.7.3 opencv-1.2.3
nagus keep nagus.json

nagus view servers
nagus view packages
nagus view nagus.json

nagus stash c:\nagus_stash\
```

#!/bin/bash

# Set current directory to script directory.
Dir=$(cd "$(dirname "$0")" && pwd)
cd $Dir
# Init vars
VERSION=""

function finalCleanUp(){
    if [ -d "$Dir/tmp" ]; then
        echo "Clean: $Dir/tmp"
        rm -rf $Dir/tmp
    fi
}

# Create folder where we move our created deb packages
if [ ! -d "$Dir/debs" ]; then 
mkdir $Dir/debs
fi

# Get package version.
if [ ! -d "$Dir/tmp/version" ]; then 
mkdir -p $Dir/tmp/version
cd $Dir/tmp/version
wget https://raw.githubusercontent.com/MrAlex94/Waterfox/master/browser/config/version_display.txt
fi

if [ -f "$Dir/tmp/version/version_display.txt" ]; then
    VERSION=$(<$Dir/tmp/version/version_display.txt)
else
    echo "Unable to get current build version!"
    exit 1    
fi

# Generate template directories
if [ ! -d "$Dir/tmp/waterfox-$VERSION" ]; then
    mkdir $Dir/tmp/waterfox-$VERSION
fi

# Copy deb templates
if [ -d "$Dir/wf/debian" ]; then
	cp -r $Dir/wf/debian/ $Dir/tmp/waterfox-$VERSION/
else
    echo "Unable to locate deb templates!"
    exit 1 
fi

# Copy latest build
	cd $Dir/tmp/waterfox-$VERSION
	wget https://storage-waterfox.netdna-ssl.com/releases/linux64/installer/waterfox-$VERSION.en-US.linux-x86_64.tar.bz2
	tar jxf waterfox-$VERSION.en-US.linux-x86_64.tar.bz2
	if [ -d "$Dir/tmp/waterfox-$VERSION/waterfox" ]; then
	mv $Dir/tmp/waterfox-$VERSION/waterfox/browser/features/ $Dir/tmp/waterfox-$VERSION
else
    echo "Unable to Waterfox package files, Please check the build was created and packaged successfully!"
    exit 1     
fi

# Generate change log template
CHANGELOGDIR=$Dir/tmp/waterfox-$VERSION/debian/changelog
if grep -q -E "__TIMESTAMP__" "$CHANGELOGDIR" ; then
    DATE=$(date --rfc-2822)
    sed -i "s|__TIMESTAMP__|$DATE|" "$CHANGELOGDIR"
else
    echo "An error occured when trying to generate $CHANGELOGDIR information!"
    exit 1  
fi

# Make sure correct permissions are set
chmod  755 $Dir/tmp/waterfox-$VERSION/debian/waterfox.prerm
chmod  755 $Dir/tmp/waterfox-$VERSION/debian/waterfox.postinst
chmod 755 $Dir/tmp/waterfox-$VERSION/debian/rules
chmod 755 $Dir/tmp/waterfox-$VERSION/debian/waterfox.sh

# Remove unnecessary files
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/dictionaries
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/updater
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/updater.ini
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/update-settings.ini
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/precomplete
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/removed-files

# Build .deb package (Requires devscripts to be installed sudo apt install devscripts). Arch and based Linux needs -d flag.
notify-send "Building deb packages!"
debuild -us -uc -d

if [ -f $Dir/tmp/waterfox_*_amd64.deb ]; then
    mv $Dir/tmp/*.deb $Dir/debs
else
    echo "Unable to move deb packages the file maybe missing or had errors during creation!"
   exit 1
fi

notify-send "Deb package for APT repository complete!"
finalCleanUp

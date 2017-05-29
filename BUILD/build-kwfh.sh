#!/bin/bash

# Set current directory to script directory.
Dir=$(cd "$(dirname "$0")" && pwd)
cd $Dir

# Init vars
VERSION="5.0.1.3"

function finalCleanUp(){
    if [ -d "$Dir/tmp" ]; then
        echo "Cleaning temporary dirs"
        rm -rf $Dir/tmp
        rm -rf $Dir/tmp2
    fi
}

# Generate template directories
if [ ! -d "$Dir/tmp/kwaterfoxhelper-$VERSION" ]; then 
    mkdir -p $Dir/tmp/kwaterfoxhelper-$VERSION
fi

# Generate directory for compiling kwaterfoxhelper
if [ ! -d "$Dir/tmp2" ]; then 
    mkdir $Dir/tmp2
fi

# Copy latest build
cd $Dir/tmp2
wget https://github.com/hawkeye116477/kwaterfoxhelper/archive/v$VERSION.tar.gz
tar xzf v$VERSION.tar.gz

# Compile kwaterfoxhelper
cd ./kwaterfoxhelper-$VERSION
cmake ./
make

# Copy compiled files
if [ -f "$Dir/tmp2/kwaterfoxhelper-$VERSION/kwaterfoxhelper" ] && [ -f "$Dir/tmp2/kwaterfoxhelper-$VERSION/kwaterfoxhelper.notifyrc" ]; then
    cp $Dir/tmp2/kwaterfoxhelper-$VERSION/kwaterfoxhelper $Dir/tmp/kwaterfoxhelper-$VERSION/
    cp $Dir/tmp2/kwaterfoxhelper-$VERSION/kwaterfoxhelper.notifyrc $Dir/tmp/kwaterfoxhelper-$VERSION/
else
    echo "Unable to locate compiled files!"
    exit 1
fi

# Copy deb templates
if [ -d "$Dir/kwaterfoxhelper/debian" ]; then
	cp -r $Dir/kwaterfoxhelper/debian/ $Dir/tmp/kwaterfoxhelper-$VERSION/
else
    echo "Unable to locate deb templates!"
    exit 1 
fi

# Generate change log template
CHANGELOGDIR=$Dir/tmp/kwaterfoxhelper-$VERSION/debian/changelog
if grep -q -E "__TIMESTAMP__" "$CHANGELOGDIR" ; then
    DATE=$(date --rfc-2822)
    sed -i "s|__TIMESTAMP__|$DATE|" "$CHANGELOGDIR"
else
    echo "An error occured when trying to generate $CHANGELOGDIR information!"
    exit 1  
fi

# Make sure correct permissions are set
chmod 755 $Dir/tmp/kwaterfoxhelper-$VERSION/debian/rules
chmod 777 $Dir/tmp/kwaterfoxhelper-$VERSION/kwaterfoxhelper

# Build .deb package (Requires devscripts to be installed sudo apt install devscripts).
notify-send "Building deb packages!"
cd ~/waterfox-deb/BUILD/tmp/kwaterfoxhelper-$VERSION
debuild -us -uc -d

if [ -f $Dir/tmp/kwaterfoxhelper_*_amd64.deb ]; then
    mv $Dir/tmp/*.deb $Dir/debs
else
    echo "Unable to move deb packages the file maybe missing or had errors during creation!"
   exit 1
fi


notify-send "Deb & PPA complete!"
finalCleanUp

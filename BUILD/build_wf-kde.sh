#!/bin/bash

# Set current directory to script directory.
Dir=$(cd "$(dirname "$0")" && pwd)
cd $Dir

# Init vars
VERSION=""
REL=""

printf "Type release number: "
read REL

function finalCleanUp(){
    if [ -d "$Dir/tmp" ]; then
        echo "Clean: $Dir/tmp"
        rm -rf $Dir/tmp
    fi
}

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
if [ ! -d "$Dir/tmp/waterfox-kde" ]; then
    mkdir $Dir/tmp/waterfox-kde
fi

# Copy deb templates
if [ -d "$Dir/waterfox-kde/debian" ]; then
	cp -r $Dir/waterfox-kde/debian $Dir/tmp/waterfox-kde/
else
    echo "Unable to locate deb templates!"
    exit 1 
fi

# Copy latest build
cd $Dir/tmp
tar -cJf waterfox-kde_$VERSION.orig.tar.xz  --exclude ./.git --exclude ./.github --exclude ./.mozconfig --exclude ./.mozconfig_android --exclude ./.vscode -C ~/git/Waterfox .	

# Generate change log template
CHANGELOGDIR=$Dir/tmp/waterfox-kde/debian/changelog
if grep -q -E "__VERSION__|__TIMESTAMP__" "$CHANGELOGDIR" ; then
    sed -i "s|__VERSION__|$VERSION-$REL|" "$CHANGELOGDIR"
    DATE=$(date --rfc-2822)
    sed -i "s|__TIMESTAMP__|$DATE|" "$CHANGELOGDIR"
else
    echo "An error occured when trying to generate $CHANGELOGDIR information!"
    exit 1  
fi


# Build packages for Launchpad. Arch and based Linux needs -d flag.
cd $Dir/tmp/waterfox-kde
notify-send "Building packages!"
debuild -S -sa -d
dput myppa $Dir/tmp/waterfox-kde_${VERSION}-${REL}_source.changes

notify-send "Packaging complete!"
finalCleanUp

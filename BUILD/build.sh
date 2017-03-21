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
		rm -rf $Dir/version
    fi
}


# Get package version.
if [ ! -d "$Dir/version" ]; then 
mkdir $Dir/version
cd $Dir/version
wget https://raw.githubusercontent.com/MrAlex94/Waterfox/master/browser/config/version_display.txt
fi
if [ -f "$Dir/version/version_display.txt" ]; then
    VERSION=$(<$Dir/version/version_display.txt)
else
    echo "Unable to get current build version!"
    exit 1    
fi


# Generate template directories
if [ ! -d "$Dir/tmp" ]; then 
    mkdir $Dir/tmp
    mkdir $Dir/tmp/waterfox-$VERSION
	fi

# Check if kwaterfoxhelper is available
if [ ! -f $Dir/wf/debian/kwaterfoxhelper ]; then
    echo "File kwaterfoxhelper is not available!"
   exit 1
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
	#wget https://storage-waterfox.netdna-ssl.com/releases/linux64/installer/waterfox-$VERSION.en-US.linux-x86_64.tar.bz2
	#tar jxf waterfox-$VERSION.en-US.linux-x86_64.tar.bz2
    cp -r ~/Waterfox/objdir/dist/waterfox $Dir/tmp/waterfox-$VERSION
	if [ -d "$Dir/tmp/waterfox-$VERSION/waterfox" ]; then
	mv $Dir/tmp/waterfox-$VERSION/waterfox/browser/features $Dir/tmp/waterfox-$VERSION
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
chmod  755 $Dir/tmp/waterfox-$VERSION/debian/waterfox.postrm
chmod 755 $Dir/tmp/waterfox-$VERSION/debian/rules
chmod 755 $Dir/tmp/waterfox-$VERSION/debian/waterfox.sh
chmod 755 $Dir/tmp/waterfox-$VERSION/debian/kwaterfoxhelper


# Remove unnecessary files
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/dictionaries
#rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/updater
#rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/updater.ini
#rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/update-settings.ini
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/precomplete
rm -rf $Dir/tmp/waterfox-$VERSION/waterfox/removed-files

# Build .deb package (Requires devscripts to be installed sudo apt install devscripts)
notify-send "Building deb package!"
debuild -us -uc 

if [ -f $Dir/tmp/waterfox_*_amd64.deb ]; then
    mv $Dir/tmp/*.deb $Dir/debs
else
    echo "Unable to move deb packages the file maybe missing or had errors during creation!"
   exit 1
fi

notify-send "Deb & PPA complete!"
finalCleanUp

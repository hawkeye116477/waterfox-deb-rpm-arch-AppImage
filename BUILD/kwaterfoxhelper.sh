debuild -us -uc -d -S
sudo pbuilder --build                                               \
                --distribution xenial                                 \
                --architecture amd64                                  \
                --basetgz /var/cache/pbuilder/base.tgz   \
                ~/waterfox-deb/BUILD/tmp/waterfox_$VERSION.dsc
                
                if [ -f /var/cache/pbuilder/result/waterfox_*_amd64.deb ]; then
    cp /var/cache/pbuilder/result/*.deb $Dir/debs
else
    echo "Unable to move deb packages, files maybe missing or had errors during creation!"
   exit 1
fi

sudo rm -rf /var/cache/pbuilder/result/*

## Adding repository

Run these commands to add this repostory to your APT sources list: 

`echo "deb https://dl.bintray.com/hawkeye116477/waterfox-deb release main" | sudo tee -a /etc/apt/sources.list`

And the public GPG key:

`curl https://bintray.com/user/downloadSubjectPublicKey?username=hawkeye116477 | sudo apt-key add -`

You can download and install the packages after you update the APT package index: 

`sudo apt-get update`

### Note: Language packs and KDE integration features are available as separate packages to install from apt repository!

## Getting automatic notifications about new versions of packages

waterfox, waterfox-kde & locales: <a href='https://bintray.com/hawkeye116477/waterfox-deb/waterfox?source=watch' alt='Get automatic notifications about new "waterfox" versions'><img src='https://www.bintray.com/docs/images/bintray_badge_color.png'></a>

kwaterfoxhelper: <a href='https://bintray.com/hawkeye116477/waterfox-deb/kwaterfoxhelper?source=watch' alt='Get automatic notifications about new "kwaterfoxhelper" versions'><img src='https://www.bintray.com/docs/images/bintray_badge_bw.png'></a>

## Source

Waterfox packages were generated with files from <a href="https://www.waterfoxproject.org/downloads">official Waterfox website</a>.

Waterfox KDE Plasma Edition was generated with files from <a href="https://github.com/MrAlex94/Waterfox">official Waterfox GitHub</a> and contains <a href="http://www.rosenauer.org/hg/mozilla/file/tip/">openSUSE's KDE patches</a>, <a href="https://raw.githubusercontent.com/manjaro/packages-community/master/firefox-kde/no-crmf.diff">no-crmf.diff</a> and <a href="https://github.com/manjaro/packages-community/blob/master/firefox-kde/fix-wifi-scanner.diff">fix-wifi-scanner.diff</a>.

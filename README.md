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

## Patches

Latest Waterfox KDE Plasma Edition contains following patches: <a href="http://www.rosenauer.org/hg/mozilla/file/tip/">openSUSE's KDE patches (firefox-kde.patch & mozilla-kde.patch)</a>, <a href="https://github.com/hawkeye116477/Waterfox/tree/plasma/_Plasma_Build">no-crmf.diff, clip-ft-glyph.diff, disable_e10s.patch, fix_waterfox_browser-kde_xul.patch, harmony-fix.diff, pgo_fix_missing_kdejs.patch, wifi-disentangle.patch, wifi-fix-interface.patch</a> and <a href="http://www.rosenauer.org/hg/mozilla/file/tip/">mozilla-ucontext.patch</a>.

## Problems
When you have some problem with my packages or repository, for first check opened or pinned [issues](https://github.com/hawkeye116477/waterfox-deb-rpm-arch-AppImage/issues?q=is%3Aopen+is%3Aissue) and [discussions](https://github.com/hawkeye116477/waterfox-deb-rpm-arch-AppImage/discussions?discussions_q=is%3Aopened).

## Adding repository/direct download

* If you're using Arch, Debian or Ubuntu with KDE:

[Click to see instructions for waterfox-kde-full.](https://software.opensuse.org//download.html?project=home%3Ahawkeye116477%3Awaterfox&package=waterfox-kde-full)

* If you're using other environment than KDE (Gnome, XFCE, etc) or other distro than Arch, Debian or Ubuntu:

[Click to see instructions for waterfox-kde.](https://software.opensuse.org//download.html?project=home%3Ahawkeye116477%3Awaterfox&package=waterfox-kde)


------
### Note 1: KDE package is compatible with other DE also and doesn't depend on KDE libs. Hovewer for KDE I recommend installing package waterfox-kde-full, which also installs other depends required for proper working of KDE integration features.

### Note 2: Grabbing packages directly doesn't always work without errors. If you got error about unmet depends, then  you need to lookup what depends it needs (see control file for package), then download and install them manually or just do the step with adding repository instead of.

### Note 3: Language packs are available as separate packages to install from apt repository! You can also download and install it directly from [download.opensuse.org/repositories/home:/hawkeye116477:/waterfox/xUbuntu_18.04/all](https://download.opensuse.org/repositories/home:/hawkeye116477:/waterfox/xUbuntu_18.04/all).

## Downloading and installing AppImage packages (compatible with glibc 2.28+ *)

[Click to download latest Waterfox G.](https://download.opensuse.org/repositories/home:/hawkeye116477:/waterfox/AppImage/waterfox-g-latest-x86_64.AppImage.mirrorlist)

#### \* From 8.8.2024, AppImage will be built on Alma Linux 8, so distros using older glibc than 2.28 won't be supported.

## Other source files

[Click to see other source files for waterfox-kde.](https://build.opensuse.org/package/show/home:hawkeye116477:waterfox/waterfox-kde)

[Click to see other source files for Waterfox G AppImage Edition.](https://build.opensuse.org/package/show/home:hawkeye116477:waterfox/waterfox-g-appimage)

## Patches
Latest Waterfox G KDE Plasma Edition contains following patches: [github.com/hawkeye116477/waterfox-deb/tree/master/waterfox-kde/patches](https://github.com/hawkeye116477/waterfox-deb/tree/master/waterfox-kde/patches).

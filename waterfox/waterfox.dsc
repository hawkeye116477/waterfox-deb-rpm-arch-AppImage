Format: 3.0 (quilt)
Source: waterfox
Binary: waterfox
Architecture: any
Version: 6.5.10-0
Maintainer: hawkeye116477 <hawkeye116477@gmail.com>
Homepage: https://www.waterfox.net
Standards-Version: 3.9.7
Build-Depends: debhelper (>= 9), libgtk-3-dev, libdbus-glib-1-dev, libpulse-dev, libasound2-dev, yasm, build-essential, libxt-dev, python3 (>= 3.7) | python3.7, zip, unzip, cargo (>= 0.78) | cargo-1.80, libgl1-mesa-dev, binutils-avr, clang (>= 5.0) | clang-14 | clang-15 | clang-16 | clang-17 | clang-19, llvm-dev (>= 5.0) | llvm-14-dev | llvm-15-dev | llvm-16-dev | llvm-17-dev | llvm-19-dev, lld (>= 5.0) | lld-14 | lld-15 | lld-16 | lld-17 | lld-19, rustc (>= 1.78.0~) | rustc-1.80, libxext-dev, libglib2.0-dev, libstartup-notification0-dev, libcurl4-openssl-dev, libiw-dev, mesa-common-dev, libxrender-dev, dbus-x11, xvfb, libx11-dev, libx11-xcb-dev, apt-utils, locales, autotools-dev, libjpeg-dev, zlib1g-dev, libreadline-dev, dpkg-dev, libevent-dev, libjsoncpp-dev, xfonts-base, xauth, lsb-release, cbindgen (>= 0.26.0~), nodejs (>= 12.22.1) | nodejs-mozilla (>= 12.22.1), libjack-dev, nasm (>= 2.14) | nasm-mozilla (>= 2.14), libclang-dev (>= 5.0) | libclang-14-dev | libclang-15-dev | libclang-16-dev | libclang-17-dev | libclang-19-dev, libclang-rt-dev | libclang-rt-15-dev | libclang-rt-16-dev | libclang-rt-17-dev | libclang-rt-19-dev, libstdc++6 (>= 7.0) | gcc-10, bc, libpci-dev, python3-distutils | python3-setuptools, python3-typing-extensions
Package-List:
 waterfox deb web optional arch=any
Files:
 0000000000000000000000000000000 1 waterfox.orig.tar.gz
 0000000000000000000000000000000 1 waterfox.debian.tar.xz
# https://github.com/openSUSE/obs-build/pull/147
DEBTRANSFORM-RELEASE: 1
DEBTRANSFORM-TAR: waterfox-6.5.10.tar.gz

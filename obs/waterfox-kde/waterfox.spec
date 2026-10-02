#
# spec file for package waterfox-kde
#
#
# Please submit bugfixes or comments via https://build.opensuse.org/package/show/home:hawkeye116477:waterfox/waterfox-kde or https://www.reddit.com/r/waterfox/
#

# general build definitions
%define progname waterfox
%define progdir %{_prefix}/%_lib/waterfox
%define pkgname  waterfox
%define appname  Waterfox
%define desktop_file_name %{progname}
%define __provides_exclude ^lib.*\\.so.*$
%global __requires_exclude ^(%%(find %{buildroot}%{progdir} -name '*.so' | xargs -n1 basename | sort -u | paste -s -d '|' -))
%define source_prefix  %{pkgname}-%{version}


%if 0%{?sle_version} && 0%{?sle_version} == 150400
%define do_lpgo 0
%else
%define do_lpgo 1
%endif

%define use_lld 1


%if 0%{?fedora}
%define use_lld 0
%else
%define use_lld 1
%endif

%if 0%{?fedora} && 0%{?fedora} >= 39
%define use_system_nss 1
%endif

%if 0%{?sle_version} == 150200 || 0%{?suse_version} == 1550 || 0%{?fedora}
%define disable_eh 1
%else
%define disable_eh 0
%endif

%if 0%{?fedora} && 0%{?fedora} >= 36
%undefine _package_note_file
%endif

%if 0%{?fedora}
%undefine _package_note_flags
# for https://bugzilla.redhat.com/show_bug.cgi?id=2184553
%global _package_note_status 0
%endif

%define _lto_cflags %{nil}

%if !0%{?is_opensuse}
%global toolchain clang
%endif

%if 0%{?centos_version} == 700
%define versioned_python_package rh-python38
%define python_binary_name rh-python38
%endif

%if 0%{?sle_version} >= 150400 && 0%{?sle_version} <= 150600
%define versioned_python_package python39
%define python_binary_name python3.9
%endif

%if 0%{?rhel} == 8 || 0%{?fedora} >= 39
%define versioned_python_package python3.11
%define python_binary_name python3.11
%endif

Name:           %{pkgname}
BuildRequires:  pkgconfig(gl)
BuildRequires:  alsa-lib-devel

%if 0%{?suse_version}
BuildRequires: dbus-1
%endif

%if 0%{?mageia}
BuildRequires: dbus
%endif

%if !0%{?mageia} && !0%{?suse_version}
BuildRequires: dbus-daemon
%endif

BuildRequires:  pkgconfig(dbus-glib-1)

BuildRequires:  clang-devel
BuildRequires:  llvm-devel

%if 0%{?fedora}
BuildRequires:  mold
%endif

BuildRequires:  libdrm-devel

BuildRequires:  cargo >= 0.78
%if 0%{?suse_version}
BuildRequires:  libiw-devel
BuildRequires:  myspell-dictionaries
%endif
BuildRequires:  libnotify-devel
BuildRequires:  libproxy-devel

%if 0%{?versioned_python_package:1}
BuildRequires:  %{versioned_python_package}
%else
BuildRequires:  pkgconfig(python3) >= 3.7
BuildRequires:  python3 >= 3.7
%endif
%if 0%{?sle_version} <= 150600 && 0%{?sle_version}
BuildRequires: %{versioned_python_package}-curses
%endif
%if 0%{?suse_version} >= 1699 && 0%{?suse_version}
BuildRequires: python3-curses
%endif
BuildRequires:  pkgconfig(jack)
%if 0%{?suse_version}
BuildRequires:  rust-cbindgen >= 0.26
%else
BuildRequires:  cbindgen >= 0.26
%endif
BuildRequires:  rust >= 1.78
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  pkgconfig(xt)
BuildRequires:  yasm
BuildRequires:  zip
%if 0%{?suse_version} && 0%{?suse_version} < 1550
BuildRequires:  pkgconfig(gconf-2.0)
%endif
BuildRequires:  pkgconfig(gdk-x11-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.22
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.18.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4.0
BuildRequires:  pkgconfig(gtk+-unix-print-2.0)
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  libcurl-devel
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpulse)
%if 0%{?centos_version} == 700
BuildRequires:  rh-nodejs14-nodejs
%else
BuildRequires:  nodejs >= 12.22.1
%endif
BuildRequires:  nasm >= 2.14.02
%if 0%{?do_lpgo}
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:  xorg-x11-server-Xvfb
%endif
%if 0%{?suse_version}
BuildRequires:  xvfb-run
%endif
%if 0%{?mageia}
BuildRequires:  x11-server-xvfb
%endif
%endif
%if 0%{?use_lld}
BuildRequires:  lld
%else
BuildRequires:  binutils
%endif
%if 0%{?use_system_nss}
BuildRequires:  pkgconfig(nspr) >= 4.35
BuildRequires:  pkgconfig(nss) >= 3.101
%endif

%if 0%{?el7}
BuildRequires:    nss-softokn
BuildRequires:    sqlite-devel
BuildRequires:    zlib-devel
BuildRequires:    pkgconfig
BuildRequires:    gawk
BuildRequires:    psmisc
BuildRequires:    perl-interpreter
BuildRequires:    xmlto
%endif

%if 0%{?rhel} || 0%{?fedora} || 0%{?mageia}
BuildRequires:  compiler-rt
%else 
BuildRequires: libclang_rt.memprof-x86_64.so()(64bit)
%endif

%if 0%{?fedora}
BuildRequires:  pipewire-devel
%endif

%if 0%{?fedora} >= 36
BuildRequires:  libavcodec-free-devel
%endif

%if 0%{?suse_version}
BuildRequires:  memory-constraints m4
%endif

BuildRequires:  pkgconfig(xtst)

%if 0%{?fedora_version} > 37
BuildRequires:  rustfmt
%endif

%if 0%{?centos} == 7
BuildRequires:  epel-rpm-macros
%endif

%if 0%{?is_opensuse}
%if 0%{?suse_version} < 1550 && 0%{?sle_version} <= 150600 && 0%{?sle_version} > 150400
BuildRequires:  gcc12-c++
%endif
%if 0%{?sle_version} == 150400
BuildRequires: gcc10-c++
%endif
%endif

%if 0%{?do_lpgo}
BuildRequires:  pkgconfig(libpci)
%endif

%if 0%{?is_opensuse}
BuildRequires: Mesa-devel
%else
BuildRequires: mesa-dri-drivers
%endif



# libavcodec is required for H.264 support but the
# openSUSE version is currently not able to play H.264
# therefore the Packman version is required
# minimum version of libavcodec is 53
%if 0%{?suse_version}
Recommends:     libavcodec-full >= 0.10.16
%endif

%if 0%{?suse_version} || 0%{?fedora}
Recommends:     libcanberra.so.0()(64bit)
Suggests:       pulseaudio-libs
%endif
Obsoletes:      waterfox-current-kpe <= 2020.11
Obsoletes:      waterfox-g4-kpe <= 1.2
Obsoletes:      waterfox-g-kpe < %{version}
Obsoletes:      waterfox-kde < %{version}
Version:        6.6.3
Release:        1
Provides:       web_browser
Provides:       appdata()
Provides:       appdata(waterfox.appdata.xml)
Provides:       %{progname} = %{version}
Summary:        Customizable privacy conscious web browser with better integration with KDE and primary support for webextensions
License:        MPL-2.0
Group:          Productivity/Networking/Web/Browsers
Url:            https://www.waterfox.net/
Source0:        %source_prefix.tar.gz
Source1:        waterfox.desktop
Source2:        vendor.js
Source4:        distribution.ini
Source5:        waterfox.1
Source6:        syspref.js
Source7:        tar_stamps
Source9:        waterfox.appdata.xml.in
Source10:       waterfox-wayland.desktop
Source11:       locales.shipped
Source12:       kde.js

Patch5: mozilla-ntlm-full-path.patch
Patch7: libavcodec58_91.patch
Patch8: fix-langpack-id.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?centos_version}
Requires:         %{progname}-i18n-all
%endif
Requires(post):   coreutils shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

%if 0%{?fedora} || 0%{?rhel} >= 8
%define debug_package %{nil}
%endif
%description
 Waterfox focuses on giving users choice while also helping make the world a better place. Watefox is partners with Ecosia, a search engine that plants trees with its generated revenues. The browser itself is focused on power users, which lets you make the important decisions. There is no plugin whitelist, you can run whichever extensions you like and absolutely no data or telemetry is sent back to Mozilla or the Waterfox project.
 Waterfox is powered by Mozilla Firefox source code.

%define lang_subpkg(f:p:l:) \
%define filecode %{-f:%{-f*}}%{!-f:%{error:Language file code not defined}} \
%define pkgcode %{-p:%{-p*}}%{!-p:%{error:Language package code not defined}} \
%define langname %{-l:%{-l*}}%{!-l:%{error:Language name not defined}} \
\
%package -n %{progname}-i18n-%{filecode}\
%{-l:Summary: %{langname} language pack for %{appname}\
Group: System/Localization\
Obsoletes:      waterfox-current-i18n-%{filecode} <= 2020.11\
Obsoletes:      waterfox-g4-i18n-%{filecode} <= 1.2\
Obsoletes:      waterfox-g-i18n-%{filecode} < %{version}\
Requires:       %{progname} = %{version}\
%if 0%{?mageia} \
Supplements:    (%{progname} = %{version} and locales-%{pkgcode}) \
%endif \
%if 0%{?fedora} \
Supplements:    (%{progname} = %{version} and (langpacks-%{pkgcode} or kde-l10n-%{pkgcode})) \
%endif \
%if 0%{?suse_version} \
Supplements:    (%{progname} = %{version} and (yast2-trans-%{pkgcode} or translation-update-%{pkgcode} or kde-l10n-%{pkgcode})) \
%endif \
\
%description -n %{progname}-i18n-%{filecode}\
This package contains %{langname} translations for Waterfox G}\
\
%files -n  %{progname}-i18n-%{filecode}\
%defattr(-,root,root)\
%dir %{progdir}/browser/extensions/\
%{progdir}/browser/extensions/langpack-%{filecode}@l10n.waterfox.net.xpi\

%if 0%{?centos_version} == 700
%package -n %{progname}-i18n-all
Summary: All language packages for %{appname}
Group: System/Localization
Obsoletes:      waterfox-current-i18n-all <= 2020.11
Obsoletes:      waterfox-g4-i18n-all <= 1.2
Obsoletes:      waterfox-g-i18n-all < %{version}

%description -n %{progname}-i18n-all
This package contains all translations for Waterfox G

%files -n %{progname}-i18n-all
%defattr(-,root,root)
%{progdir}/browser/extensions/
%endif

%package -n %{progname}-kde-full
Summary: KDE integration configuration
Group: System/GUI/KDE
%if 0%{?suse_version}
Supplements:    packageand(waterfox:plasma5-desktop)
Supplements:    packageand(waterfox:plasma6-desktop)
%endif
%if 0%{?mageia} || 0%{?fedora} || 0%{?rhel} >= 8
Supplements:    packageand(waterfox:plasma-desktop)
%endif
Requires: xdg-desktop-portal-kde

%description -n %{progname}-kde-full
This package contains settings allowing to use KDE file dialogs and mimetypes.

%files -n %{progname}-kde-full
%defattr(-,root,root)
%{progdir}/browser/defaults/preferences/kde.js

%if 0%{?rhel} >= 8 || 0%{?suse_version} || 0%{?fedora} || 0%{?mageia}
%lang_subpkg -f ar -p ar -l %{quote:Arabic}
%lang_subpkg -f cs -p cs -l %{quote:Czech}
%lang_subpkg -f da -p da -l %{quote:Danish}
%lang_subpkg -f de -p de -l %{quote:German}
%lang_subpkg -f el -p el -l %{quote:Greek}
%lang_subpkg -f en-GB -p en_GB -l %{quote:English (British)}
%lang_subpkg -f es-ES -p es -l %{quote:Spanish (Spain)}
%lang_subpkg -f es-MX -p es_MX -l %{quote:Spanish (Mexico)}
%lang_subpkg -f fr -p fr -l %{quote:French}
%lang_subpkg -f hu -p hu -l %{quote:Hungarian}
%lang_subpkg -f id -p id -l %{quote:Indonesian}
%lang_subpkg -f it -p it -l %{quote:Italian}
%lang_subpkg -f ja -p ja -l %{quote:Japanese}
%lang_subpkg -f ko -p ko -l %{quote:Korean}
%lang_subpkg -f lt -p lt -l %{quote:Lithuanian}
%lang_subpkg -f nl -p nl -l %{quote:Dutch}
%lang_subpkg -f nn-NO -p nn -l %{quote:Norwegian (Nynorsk)}
%lang_subpkg -f pl -p pl -l %{quote:Polish}
%lang_subpkg -f pt-BR -p pt_BR -l %{quote:Portuguese (Brazilian)}
%lang_subpkg -f pt-PT -p pt -l %{quote:Portuguese (Portugal)}
%lang_subpkg -f ru -p ru -l %{quote:Russian}
%lang_subpkg -f sv-SE -p sv -l %{quote:Swedish}
%lang_subpkg -f th -p th -l %{quote:Thai}
%lang_subpkg -f vi -p vi -l %{quote:Vietnamese}
%lang_subpkg -f zh-CN -p zh_CN -l %{quote:Chinese (Simplified)}
%lang_subpkg -f zh-TW -p zh_TW -l %{quote:Chinese (Traditional)}
%endif

%package -n %{progname}-wayland
Summary: Waterfox Wayland launcher.
Requires: %{progname} = %{version}
Obsoletes:      waterfox-current-wayland <= 2020.11
Obsoletes:      waterfox-g-wayland < %{version}
%if 0%{?fedora} || 0%{?rhel} >= 8
Supplements:    packageand(waterfox:xorg-x11-server-Xwayland)
%endif
%if 0%{?suse_version}
Supplements:    packageand(waterfox:xorg-x11-server-wayland)
%endif

%description -n %{progname}-wayland
This package contains launcher and desktop file to run Waterfox G natively on Wayland.

%files -n %{progname}-wayland
%{_bindir}/waterfox-wayland
%{_datadir}/applications/waterfox-wayland.desktop

%prep
%autosetup -p1

cat > ../mozconfig <<END
ac_add_options --enable-alsa
ac_add_options --enable-pulseaudio
ac_add_options --enable-jack

ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"

# Disable unwanted features
ac_add_options --disable-debug
ac_add_options --disable-debug-symbols
ac_add_options --disable-crashreporter
ac_add_options --disable-dmd
ac_add_options --disable-geckodriver
ac_add_options --disable-bootstrap
ac_add_options --disable-profiling
ac_add_options --disable-tests
%if 0%{?disable_eh}
ac_add_options --disable-elf-hack
%endif
ac_add_options --disable-updater
ac_add_options --without-wasm-sandboxed-libraries

# Enable wanted features
ac_add_options --enable-unverified-updates
ac_add_options --enable-jxl
ac_add_options --enable-optimize
ac_add_options --enable-eme=widevine
ac_add_options --enable-rust-simd
ac_add_options --enable-application=browser
ac_add_options --enable-hardening
%if 0%{?use_lld}
ac_add_options --enable-linker=lld
%else
ac_add_options --enable-linker=mold
%endif
ac_add_options --enable-default-toolkit=cairo-gtk3-wayland
ac_add_options --allow-addon-sideload

ac_add_options --with-app-name=waterfox
ac_add_options --with-app-basename=Waterfox
ac_add_options --with-branding=waterfox/browser/branding
ac_add_options --with-distribution-id=hawkeye116477
ac_add_options --with-system-zlib
%if 0%{?use_system_nss}
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
ac_add_options --with-unsigned-addon-scopes=app,system
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 8 || 0%{?mageia} == 99
ac_add_options --with-libclang-path=`llvm-config --libdir`
%endif

ac_add_options "MOZ_ALLOW_LEGACY_EXTENSIONS=1"

export MOZ_REQUIRE_SIGNING=
export MOZ_INCLUDE_SOURCE_INFO=1
export MOZ_APP_REMOTINGNAME=waterfox

%if 0%{?do_lpgo}
mk_add_options MOZ_MAKE_FLAGS="-j1"
mk_add_options MOZ_PARALLEL_BUILD="1"
%endif
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj
END

# Use correct python version for mach
%if 0%{?sle_version} == 150400 || 0%{?sle_version} == 150500 || 0%{?fedora} >= 39
sed -i -e 's|#!/usr/bin/env python3|#!/usr/bin/env %{python_binary_name}|' mach
%endif

%build
export MOZ_SOURCE_REPO=https://github.com/BrowserWorks/Waterfox
export MOZ_SOURCE_CHANGESET=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export WF_VERSION=%{version}
export GALLIUM_DRIVER=llvmpipe

echo $WF_VERSION > browser/config/version_display.txt

%if 0%{?centos_version} == 700
export LC_ALL=en_US.UTF-8
export NODEJS=/opt/rh/rh-nodejs14/root/usr/bin/node
export PATH="/opt/rh/rh-python38/root/usr/bin:$PATH"
%endif
%if 0%{?fedora} >= 39 || 0%{?suse_version} >= 1699
export CBINDGEN=/usr/bin/cbindgen
%endif
export MACH_BUILD_PYTHON_NATIVE_PACKAGE_SOURCE=system
export MOZ_NOSPAM=1
export MOZBUILD_STATE_PATH="%{_sourcedir}/mozbuild"

export CC=clang
export CXX=clang++

MOZ_OPT_FLAGS=$(echo "%{optflags}" | sed -e 's/-mtune=generic/-mtune=k8/' | sed -e 's/-fexceptions//')

# We don't want Waterfox to use CK_GCM_PARAMS_V3 in nss
%if 0%{?use_system_nss}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -DNSS_PKCS11_3_0_STRICT"
%endif
export CFLAGS="$MOZ_OPT_FLAGS"
export CXXFLAGS="$MOZ_OPT_FLAGS"

%if 0%{?is_opensuse}
MOZ_LINK_FLAGS="$LDFLAGS -fPIC -Wl,-z,relro,-z,now"
%else
MOZ_LINK_FLAGS="%{build_ldflags}"
%endif

%if 0%{?use_lld} || 0%{?fedora}
MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -Wl,--no-keep-memory -Wl,--threads=1,--thinlto-jobs=1"
%else
MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -Wl,--no-keep-memory -Wl,--no-map-whole-files -Wl,--no-mmap-output-file -Wl,--no-keep-files-mapped"
%endif

%if 0%{?mga8}
MOZ_LINK_FLAGS=$(echo "${MOZ_LINK_FLAGS}" | sed -e 's/--enable-new-dtags/--disable-new-dtags/')
%endif

export LDFLAGS="$MOZ_LINK_FLAGS"

# Do PGO + LTO
%if 0%{?do_lpgo}
  # LTO needs more open files
  ulimit -n 4096
  echo "Building instrumented browser..."
  cat >.mozconfig ../mozconfig - <<END
ac_add_options --enable-profile-generate=cross
END
  ./mach build --priority normal

  echo "Profiling instrumented browser..."
  ./mach package
  LLVM_PROFDATA=llvm-profdata \
    JARLOG_FILE="$PWD/jarlog" \
    dbus-run-session \
    xvfb-run -s "-screen 0 1920x1080x24 -nolisten local" \
    ./mach python build/pgo/profileserver.py

  stat -c "Profile data found (%s bytes)" merged.profdata
  test -s merged.profdata

  stat -c "Jar log found (%s bytes)" jarlog
  test -s jarlog

  echo "Removing instrumented browser..."
  ./mach clobber objdir

  echo "Building optimized browser..."
  cat >.mozconfig ../mozconfig - <<END
ac_add_options --enable-lto=cross
ac_add_options --enable-profile-use=cross
ac_add_options --with-pgo-profile-path="$PWD"/merged.profdata
ac_add_options --with-pgo-jarlog="$PWD"/jarlog
END
%else
cat >.mozconfig ../mozconfig - <<END
END
%endif
  ./mach build --priority normal


# Build language packages
%define njobs 0%{?jobs:%jobs}

# langpack-build can not be done in parallel easily (see https://bugzilla.mozilla.org/show_bug.cgi?id=1660943)
# Therefore, we have to have a separate obj-dir for each language
# We do this, by creating a mozconfig-template with the necessary switches
# and a placeholder obj-dir, which gets copied and modified for each language
cat << EOF > mozconfig_LANG
ac_add_options --with-app-name=waterfox
ac_add_options --with-app-basename=Waterfox
ac_add_options --with-branding=waterfox/browser/branding
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj_LANG
ac_add_options --prefix=/usr
ac_add_options --with-l10n-base=@TOPSRCDIR@/waterfox/browser/locales
ac_add_options --disable-updater
ac_add_options --disable-bootstrap
%if 0%{?use_lld}
ac_add_options --enable-linker=lld
%else
ac_add_options --enable-linker=mold
%endif
ac_add_options --without-wasm-sandboxed-libraries
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 8 || 0%{?mageia} == 99
ac_add_options --with-libclang-path=`llvm-config --libdir`
%endif
EOF

mkdir -p %{_tmppath}/extensions
sed -r '/^(ja-JP-mac|en-US|)$/d;s/ .*$//' %{SOURCE11} | cut -f1 -d":" \
    | xargs -n 1 %{?njobs:-P %njobs} -I {} /bin/sh -c '
        locale=$1
        cp mozconfig_LANG $RPM_BUILD_DIR/mozconfig_$locale
        sed -i "s|obj_LANG|obj_$locale|" $RPM_BUILD_DIR/mozconfig_$locale
        export MOZCONFIG=$RPM_BUILD_DIR/mozconfig_$locale
        ./mach build config/nsinstall langpack-$locale
        cp -L ../obj_$locale/dist/linux-*/xpi/waterfox-$WF_VERSION.$locale.langpack.xpi \
            %{_tmppath}/extensions/langpack-$locale@l10n.waterfox.net.xpi
' -- {}

%install
export MOZ_SOURCE_REPO=https://github.com/BrowserWorks/Waterfox
export MOZ_SOURCE_CHANGESET=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export WF_VERSION=%{version}

%if 0%{?centos_version} == 700
export LC_ALL=en_US.UTF-8
export NODEJS=/opt/rh/rh-nodejs14/root/usr/bin/node
export PATH="/opt/rh/rh-python38/root/usr/bin:$PATH"
%endif
export MACH_BUILD_PYTHON_NATIVE_PACKAGE_SOURCE=system
export MOZ_NOSPAM=1
export MOZBUILD_STATE_PATH="%{_sourcedir}/mozbuild"

DESTDIR=%{buildroot} ./mach install

%{__install} -Dm 644 %{SOURCE2} %{buildroot}%{progdir}/browser/defaults/preferences/vendor.js

%{__install} -Dm 644 %{SOURCE12} %{buildroot}%{progdir}/browser/defaults/preferences/kde.js

cat > %{buildroot}%{progdir}/browser/defaults/preferences/spellcheck.js <<END
pref("spellchecker.dictionary_path", "/usr/share/myspell");
END

for i in 16 32 48 64 128; do
  %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  ln -Tsrf %{buildroot}%{progdir}/browser/chrome/icons/default/default$i.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{progname}.png
done

%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/192x192/apps
%{__install} -Dm644 waterfox/browser/branding/content/about-logo.png \
  "%{buildroot}%{_datadir}/icons/hicolor/192x192/apps/%{progname}.png"

%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/384x384/apps
%{__install} -Dm644 waterfox/browser/branding/content/about-logo@2x.png \
  "%{buildroot}%{_datadir}/icons/hicolor/384x384/apps/%{progname}.png"

%{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE10}

# Add manpage
%{__install} -p -Dm 644 %{SOURCE5} %{buildroot}%{_mandir}/man1/%{progname}.1

# Add appdata
export TODAY_DATE=$(date +%Y-%m-%d)
mkdir -p %{buildroot}%{_datadir}/appdata
sed -i "s/__DATE__/$TODAY_DATE/g" %{SOURCE9}
sed -e "s/__VERSION__/$WF_VERSION/g" %{SOURCE9} > %{buildroot}%{_datadir}/appdata/waterfox.appdata.xml

# Add distribution.ini
%{__mkdir_p} %{buildroot}%{progdir}/distribution
%{__cp} %{SOURCE4} %{buildroot}%{progdir}/distribution/distribution.ini

# Use system-provided dictionaries
rm -rf "%{buildroot}%{progdir}/dictionaries"

# Add syspref.js for setting preferences for all users
%{__mkdir_p} %{buildroot}/etc/%{progname}
%{__cp} %{SOURCE6} %{buildroot}/etc/%{progname}
ln -Tsrf %{buildroot}/etc/%{progname}/syspref.js %{buildroot}%{progdir}/browser/defaults/preferences/syspref.js

# Install a wrapper to avoid confusion about binary path
%{__install} -Dm755 /dev/stdin "%{buildroot}%{_bindir}/%{progname}" <<END
#!/bin/sh
exec %{progdir}/waterfox "\$@"
END

# Wrapper for Wayland
install -Dm755 /dev/stdin "%{buildroot}%{_bindir}/waterfox-wayland" <<END
#!/bin/bash
#
# Run Waterfox G under Wayland
#
export MOZ_ENABLE_WAYLAND=1
exec %{progdir}/waterfox "\$@"
END

# Backwards compatibility symlinks
ln -Tsrf "%{buildroot}%{_bindir}/waterfox" "%{buildroot}%{_bindir}/waterfox-g"

# Add langpacks
%{__mkdir_p} %{buildroot}%{progdir}/browser/extensions
%{__install} -Dm644 %{_tmppath}/extensions/* %{buildroot}%{progdir}/browser/extensions

%post
# update mime and desktop database
%mime_database_post
%desktop_database_post
%icon_theme_cache_post
exit 0

%postun
%icon_theme_cache_postun
%desktop_database_postun
%mime_database_postun
exit 0

%files
%defattr(-,root,root)
%{progdir}
%doc %{_mandir}/man1/*
%{_datadir}/applications/%{progname}.desktop
%{_bindir}/%{progname}
%{_bindir}/waterfox
%{_bindir}/waterfox-g
%dir /etc/%{progname}
%config /etc/%{progname}/syspref.js
%{_datadir}/icons/hicolor/16x16/apps/%{progname}.png
%{_datadir}/icons/hicolor/32x32/apps/%{progname}.png
%{_datadir}/icons/hicolor/48x48/apps/%{progname}.png
%{_datadir}/icons/hicolor/64x64/apps/%{progname}.png
%{_datadir}/icons/hicolor/128x128/apps/%{progname}.png
%{_datadir}/icons/hicolor/192x192/apps/%{progname}.png
%{_datadir}/icons/hicolor/384x384/apps/%{progname}.png
%{_datadir}/appdata/
%dir %{_datadir}/icons/hicolor/384x384
%dir %{_datadir}/icons/hicolor/384x384/apps
%exclude %dir %{progdir}/browser/extensions
%exclude %{progdir}/browser/extensions
%exclude %{progdir}/browser/defaults/preferences/kde.js

%changelog

%clean
rm -rf %{buildroot}
rm -rf %{_tmppath}/extensions

#
# spec file for package waterfox-classic
#
#
# Please submit bugfixes or comments via https://build.opensuse.org/package/show/home:hawkeye116477:waterfox/waterfox or https://www.reddit.com/r/waterfox/
#

# general build definitions
%define progname waterfox-classic
%define progdir %{_prefix}/%_lib/%{progname}
%define pkgname  waterfox-classic
%define appname  waterfox-classic
%define desktop_file_name %{progname}
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*)$
%define source_prefix  %{appname}-%{version}

Name:           %{pkgname}
BuildRequires:  pkgconfig(gl)
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(dbus-glib-1)

BuildRequires:  clang-devel
BuildRequires:  llvm-devel

BuildRequires:  cargo >= 0.38
%if 0%{?suse_version}
BuildRequires:  libiw-devel
BuildRequires:  python2-xml
BuildRequires:  myspell-dictionaries
%endif
BuildRequires:  libnotify-devel
BuildRequires:  libproxy-devel
BuildRequires:  python2-devel
BuildRequires:  rust >= 1.38
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  pkgconfig(xt)
BuildRequires:  yasm
BuildRequires:  zip
%if 0%{?suse_version} < 1550
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

BuildRequires:  libstdc++-static

BuildRequires:  nasm

# libavcodec is required for H.264 support but the
# openSUSE version is currently not able to play H.264
# therefore the Packman version is required
# minimum version of libavcodec is 53
%if 0%{?suse_version}
Recommends:     libavcodec-full >= 0.10.16
%endif

%if 0%{?suse_version} || 0%{?fedora}
Recommends:     libcanberra.so.0()(64bit)
Suggests:     pulseaudio-libs
%endif
Version:        56.2.12
Release:        0
Provides:       web_browser
Provides:       waterfox-classic-appimage
Summary:        Free, open and private browser
License:        MPL-2.0
Group:          Productivity/Networking/Web/Browsers
Url:            https://www.waterfox.net/
Source0:        %source_prefix.tar.gz
Source1:        waterfox-classic.desktop
Source2:        vendor.js
Source3:        updates.js
Source4:        distribution.ini
Source5:        waterfox-classic.1
Source6:        syspref.js
Source7:        %{pkgname}.obsinfo
Source8:        waterfox-classic.appdata.xml.in

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post):   coreutils shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
%if 0%{?fedora}
%define debug_package %{nil}
%endif
%description
 Waterfox focuses on giving users choice while also helping make the world a better place. Watefox is partners with Ecosia, a search engine that plants trees with its generated revenues. The browser itself is focused on power users, which lets you make the important decisions. There is no plugin whitelist, you can run whichever extensions you like and absolutely no data or telemetry is sent back to Mozilla or the Waterfox project.
 Waterfox is powered by Mozilla Firefox source code.
 Note: Language packs are available as separate packages!

%prep
%autosetup -n %{source_prefix} -p1

%build
cd $RPM_BUILD_DIR/%source_prefix

export MOZ_SOURCE_CHANGESET=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export MOZ_SOURCE_STAMP=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export SOURCE_REPO=https://github.com/WaterfoxCo/Waterfox-Classic
export source_repo=https://github.com/WaterfoxCo/Waterfox-Classic
export MOZ_SOURCE_REPO=https://github.com/WaterfoxCo/Waterfox-Classic
export MOZ_NOSPAM=1

%if 0%{?centos_version} == 700
export PATH=/opt/rh/llvm-toolset-7/root/usr/bin:$PATH
%endif

cat >.mozconfig <<END
export CC=clang
export CXX=clang++

ac_add_options --enable-optimize="-O2 -march=nocona -mtune=nocona -w"
ac_add_options --target=x86_64-pc-linux-gnu

ac_add_options --enable-alsa
ac_add_options --enable-pulseaudio

mk_add_options AUTOCLOBBER=1

ac_add_options --prefix="%{_prefix}"
ac_add_options --libdir="%{_libdir}"

ac_add_options --with-app-name=waterfox-classic
ac_add_options --with-app-basename=Waterfox
ac_add_options --with-branding=browser/branding/unofficial

# Disable unwanted features
ac_add_options --disable-crashreporter
ac_add_options --disable-js-shell
ac_add_options --disable-maintenance-service
ac_add_options --disable-verify-mar
ac_add_options --disable-profiling
ac_add_options --disable-signmar
ac_add_options --disable-tests
ac_add_options --disable-stylo
#ac_add_options --disable-gconf

# Enable wanted features
ac_add_options --enable-release
ac_add_options --enable-rust-simd # on x86 requires SSE2
ac_add_options --enable-application=browser
ac_add_options --enable-eme=widevine
#ac_add_options --enable-startup-notification
ac_add_options --enable-update-channel=release
ac_add_options --enable-updater
ac_add_options --enable-hardening
ac_add_options --enable-strip

export MOZ_GECKO_PROFILER=
export MOZ_ENABLE_PROFILER_SPS=
export MOZ_PROFILING=
export MOZ_INCLUDE_SOURCE_INFO=1
END

./mach build

%install

export MOZ_SOURCE_STAMP=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export MOZ_SOURCE_REPO=https://github.com/WaterfoxCo/Waterfox-Classic
export MOZ_NOSPAM=1

DESTDIR=%{buildroot} ./mach install

%{__install} -Dm 644 %{SOURCE2} %{buildroot}%{progdir}/browser/defaults/preferences/vendor.js
%{__install} -Dm 644 %{SOURCE3} %{buildroot}%{progdir}/browser/defaults/preferences/updates.js

  for i in 16 22 24 32 48 64 128 256; do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    ln -Tsf %{progdir}/browser/chrome/icons/default/default$i.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/waterfox-classic.png
  done
  %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/192x192/apps
  %{__install} -Dm644 browser/branding/unofficial/content/about-logo.png \
    "%{buildroot}%{_datadir}/icons/hicolor/192x192/apps/waterfox-classic.png"
  %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/384x384/apps
  %{__install} -Dm644 browser/branding/unofficial/content/about-logo@2x.png \
    "%{buildroot}%{_datadir}/icons/hicolor/384x384/apps/waterfox-classic.png"

  %{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

  desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

  # Add manpage
  %{__install} -p -Dm 644 %{SOURCE5} %{buildroot}%{_mandir}/man1/waterfox-classic.1

  # Add appdata
  export TODAY_DATE=$(date +%Y-%m-%d)
  mkdir -p %{buildroot}%{_datadir}/appdata
  sed -i "s/__DATE__/$TODAY_DATE/g" %{SOURCE8}
	sed -e "s/__VERSION__/$(<browser/config/version_display.txt)/g" %{SOURCE8} > %{buildroot}%{_datadir}/appdata/waterfox-classic.appdata.xml

  # Add distribution.ini
  %{__mkdir_p} %{buildroot}%{progdir}/distribution
  %{__cp} %{SOURCE4} %{buildroot}%{progdir}/distribution/distribution.ini

  # Remove duplicated binary
  rm -rf "%{buildroot}%{progdir}/waterfox-classic-bin"

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
%{_datadir}/icons/hicolor/16x16/apps/%{progname}.png
%{_datadir}/icons/hicolor/22x22/apps/%{progname}.png
%{_datadir}/icons/hicolor/24x24/apps/%{progname}.png
%{_datadir}/icons/hicolor/32x32/apps/%{progname}.png
%{_datadir}/icons/hicolor/48x48/apps/%{progname}.png
%{_datadir}/icons/hicolor/64x64/apps/%{progname}.png
%{_datadir}/icons/hicolor/128x128/apps/%{progname}.png
%{_datadir}/icons/hicolor/192x192/apps/%{progname}.png
%{_datadir}/icons/hicolor/256x256/apps/%{progname}.png
%{_datadir}/icons/hicolor/384x384/apps/%{progname}.png
%dir %{_datadir}/icons/hicolor/384x384
%dir %{_datadir}/icons/hicolor/384x384/apps
%{_datadir}/appdata/

%changelog

%clean
rm -rf %{buildroot}

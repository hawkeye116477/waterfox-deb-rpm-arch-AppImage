#
# spec file for package waterfox-classic-kpe
#
#
# Please submit bugfixes or comments via https://build.opensuse.org/package/show/home:hawkeye116477:waterfox/waterfox-classic-kpe or https://www.reddit.com/r/waterfox/
#

# general build definitions
%define progname waterfox-classic
%define progdir %{_prefix}/%_lib/%{progname}
%define pkgname  waterfox-classic-kpe
%define appname  Waterfox Classic
%define desktop_file_name %{progname}
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*|libnss3.*|libnspr4.*|libnssutil3.*|libsmime3.*|libssl3.*)$
%define source_prefix  %{pkgname}-%{version}

%if 0%{?fedora} && 0%{?fedora} >= 36
%undefine _package_note_file
%endif

%global _lto_cflags %nil

Name:           %{pkgname}
BuildRequires:  pkgconfig(gl)
BuildRequires:  alsa-lib-devel

%if 0%{?mageia}
BuildRequires:  autoconf2.1
%else
BuildRequires:  autoconf213
%endif

BuildRequires:  pkgconfig(dbus-glib-1)


%if 0%{?suse_version} >= 1550
BuildRequires:  clang15-devel
BuildRequires:  llvm15-devel
%else
BuildRequires:  clang-devel
BuildRequires:  llvm-devel
%endif

BuildRequires:  cargo >= 1.56
%if 0%{?suse_version}
BuildRequires:  libiw-devel
BuildRequires:  python2-xml
BuildRequires:  myspell-dictionaries
%endif
BuildRequires:  libnotify-devel
BuildRequires:  libproxy-devel
BuildRequires:  python2-devel
BuildRequires:  rust >= 1.56
BuildRequires:  startup-notification-devel
BuildRequires:  unzip
BuildRequires:  pkgconfig(xt)
BuildRequires:  yasm
BuildRequires:  nasm
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
Version:        2022.11
Release:        9999
%if "%{name}" == "waterfox-classic-kpe"
%if !0%{?centos_version}
Provides:       waterfox-classic = %{version}
%endif
%define kde_helper_version 6
Provides:       waterfox-kde-version = %{kde_helper_version}
%endif
Provides:       web_browser
Provides:       appdata()
Provides:       appdata(waterfox-classic.appdata.xml)
Summary:        Free, open and private browser with patches for better integration with KDE
License:        MPL-2.0
Group:          Productivity/Networking/Web/Browsers
Url:            https://www.waterfox.net/
Source:         %source_prefix.tar.gz
Source1:        waterfox-classic.desktop
Source2:        vendor.js
Source3:        kde.js
Source4:        distribution.ini
Source5:        waterfox-classic.1
Source6:        syspref.js
Source7:        tar_stamps
Source8:        waterfox-classic.appdata.xml.in

Patch1:         classic-kde.patch
Patch2:         classic-kde-xul.patch
Patch3:         pgo_fix_missing_kdejs.patch
Patch5:         dont-statically-link-libstdc++.patch
Patch6:         waterfox-classic-webrtc-cstdint.patch
Patch7:         commasplit.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?centos_version}
Requires:         %{progname}-i18n-all
%endif
Requires(post):   coreutils shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
%if 0%{?fedora} || 0%{?centos_version} != 700
%define debug_package %{nil}
%endif
%description
 ATTENTION!!! This package reached EOL status. I recommend migration to Pale Moon or Basilisk if you want XUL, otherwise there is also waterfox-g-kpe package.
 Waterfox focuses on giving users choice while also helping make the world a better place. Watefox is partners with Ecosia, a search engine that plants trees with its generated revenues. The browser itself is focused on power users, which lets you make the important decisions. There is no plugin whitelist, you can run whichever extensions you like and absolutely no data or telemetry is sent back to Mozilla or the Waterfox project.
 Waterfox is powered by Mozilla Firefox source code.
 Note: Language packs are available as separate packages!

%define lang_subpkg(f:p:l:) \
%define filecode %{-f:%{-f*}}%{!-f:%{error:Language file code not defined}} \
%define pkgcode %{-p:%{-p*}}%{!-p:%{error:Language package code not defined}} \
%define langname %{-l:%{-l*}}%{!-l:%{error:Language name not defined}} \
\
%package -n %{progname}-i18n-%{pkgcode}\
%{-l:Summary: %{langname} language pack for %{appname}\
Group: System/Localization\
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
%description -n %{progname}-i18n-%{pkgcode}\
This package contains %{langname} translations for Waterfox Classic}\
\
%files -n  %{progname}-i18n-%{pkgcode}\
%defattr(-,root,root)\
%dir %{progdir}/browser/features/\
%{progdir}/browser/features/langpack-%{filecode}@waterfox.xpi\


%if 0%{?centos_version}
%package -n %{progname}-i18n-all
Summary: All language packages for %{appname}
Group: System/Localization

%description -n %{progname}-i18n-all
This package contains all translations for Waterfox Classic

%files -n %{progname}-i18n-all
%defattr(-,root,root)
%{progdir}/browser/features/
%endif


%if !0%{?centos_version}
%lang_subpkg -f ach -p ach -l %{quote:Acholi}
%lang_subpkg -f af -p af -l %{quote:Afrikaans}
%lang_subpkg -f an -p an -l %{quote:Aragonese}
%lang_subpkg -f ar -p ar -l %{quote:Arabic}
%lang_subpkg -f as -p as -l %{quote:Assamese}
%lang_subpkg -f ast -p ast -l %{quote:Asturian}
%lang_subpkg -f az -p az -l %{quote:Azerbaijani}
%lang_subpkg -f bg -p bg -l %{quote:Bulgarian}
%lang_subpkg -f bn-BD -p bn -l %{quote:Bengali (Bangladesh)}
%lang_subpkg -f bn-IN -p bn_IN -l %{quote:Bengali (India)}
%lang_subpkg -f br -p br -l %{quote:Breton}
%lang_subpkg -f bs -p bs -l %{quote:Bosnian}
%lang_subpkg -f ca -p ca -l %{quote:Catalan}
%lang_subpkg -f cak -p cak -l %{quote:Maya Kaqchikel}
%lang_subpkg -f cs -p cs -l %{quote:Czech}
%lang_subpkg -f cy -p cy -l %{quote:Welsh}
%lang_subpkg -f da -p da -l %{quote:Danish}
%lang_subpkg -f de -p de -l %{quote:German}
%lang_subpkg -f dsb -p dsb -l %{quote:Lower Sorbian}
%lang_subpkg -f el -p el -l %{quote:Greek}
%lang_subpkg -f en-GB -p en_GB -l %{quote:English (British)}
%lang_subpkg -f en-ZA -p en_ZA -l %{quote:English (South African)}
%lang_subpkg -f eo -p eo -l %{quote:Esperanto}
%lang_subpkg -f es-AR -p es_AR -l %{quote:Spanish (Argentina)}
%lang_subpkg -f es-CL -p es_CL -l %{quote:Spanish (Chile)}
%lang_subpkg -f es-ES -p es -l %{quote:Spanish (Spain)}
%lang_subpkg -f es-MX -p es_MX -l %{quote:Spanish (Mexico)}
%lang_subpkg -f et -p et -l %{quote:Estonian}
%lang_subpkg -f eu -p eu -l %{quote:Basque}
%lang_subpkg -f fa -p fa -l %{quote:Persian}
%lang_subpkg -f ff -p ff -l %{quote:Fulah}
%lang_subpkg -f fi -p fi -l %{quote:Finnish}
%lang_subpkg -f fr -p fr -l %{quote:French}
%lang_subpkg -f fy-NL -p fy -l %{quote:Frisian}
%lang_subpkg -f ga-IE -p ga -l %{quote:Irish}
%lang_subpkg -f gd -p gd -l %{quote:Gaelic (Scotland)}
%lang_subpkg -f gl -p gl -l %{quote:Galician}
%lang_subpkg -f gn -p gn -l %{quote:Guarani}
%lang_subpkg -f gu-IN -p gu -l %{quote:Gujarati (India)}
%lang_subpkg -f he -p he -l %{quote:Hebrew}
%lang_subpkg -f hi-IN -p hi -l %{quote:Hindi (India)}
%lang_subpkg -f hr -p hr -l %{quote:Croatian}
%lang_subpkg -f hsb -p hsb -l %{quote:Upper Sorbian}
%lang_subpkg -f hu -p hu -l %{quote:Hungarian}
%lang_subpkg -f hy-AM -p hy -l %{quote:Armenian}
%lang_subpkg -f id -p id -l %{quote:Indonesian}
%lang_subpkg -f is -p is -l %{quote:Icelandic}
%lang_subpkg -f it -p it -l %{quote:Italian}
%lang_subpkg -f ja -p ja -l %{quote:Japanese}
%lang_subpkg -f ka -p ka -l %{quote:Georgian}
%lang_subpkg -f kab -p kab -l %{quote:Kabyle}
%lang_subpkg -f kk -p kk -l %{quote:Kazakh}
%lang_subpkg -f km -p km -l %{quote:Khmer}
%lang_subpkg -f kn -p kn -l %{quote:Kannada}
%lang_subpkg -f ko -p ko -l %{quote:Korean}
%lang_subpkg -f lij -p lij -l %{quote:Ligurian}
%lang_subpkg -f lt -p lt -l %{quote:Lithuanian}
%lang_subpkg -f lv -p lv -l %{quote:Latvian}
%lang_subpkg -f mai -p mai -l %{quote:Maithili}
%lang_subpkg -f mk -p mk -l %{quote:Macedonian}
%lang_subpkg -f ml -p ml -l %{quote:Malayalam}
%lang_subpkg -f mr -p mr -l %{quote:Marathi}
%lang_subpkg -f ms -p ms -l %{quote:Malay}
%lang_subpkg -f nb-NO -p nb -l %{quote:Norwegian (Bokmål)}
%lang_subpkg -f nl -p nl -l %{quote:Dutch}
%lang_subpkg -f nn-NO -p nn -l %{quote:Norwegian (Nynorsk)}
%lang_subpkg -f or -p or -l %{quote:Oriya}
%lang_subpkg -f pa-IN -p pa -l %{quote:Punjabi (India)}
%lang_subpkg -f pl -p pl -l %{quote:Polish}
%lang_subpkg -f pt-BR -p pt_BR -l %{quote:Portuguese (Brazilian)}
%lang_subpkg -f pt-PT -p pt -l %{quote:Portuguese (Portugal)}
%lang_subpkg -f rm -p rm -l %{quote:Romansh}
%lang_subpkg -f ro -p ro -l %{quote:Romanian}
%lang_subpkg -f ru -p ru -l %{quote:Russian}
%lang_subpkg -f si -p si -l %{quote:Sinhala}
%lang_subpkg -f sk -p sk -l %{quote:Slovak}
%lang_subpkg -f sl -p sl -l %{quote:Slovenian}
%lang_subpkg -f son -p son -l %{quote:Songhai}
%lang_subpkg -f sq -p sq -l %{quote:Albanian}
%lang_subpkg -f sr -p sr -l %{quote:Serbian}
%lang_subpkg -f sv-SE -p sv -l %{quote:Swedish}
%lang_subpkg -f ta -p ta -l %{quote:Tamil}
%lang_subpkg -f te -p te -l %{quote:Telugu}
%lang_subpkg -f th -p th -l %{quote:Thai}
%lang_subpkg -f tr -p tr -l %{quote:Turkish}
%lang_subpkg -f uk -p uk -l %{quote:Ukrainian%}
%lang_subpkg -f uz -p uz -l %{quote:Uzbek}
%lang_subpkg -f vi -p vi -l %{quote:Vietnamese}
%lang_subpkg -f xh -p xh -l %{quote:Xhosa}
%lang_subpkg -f zh-CN -p zh_CN -l %{quote:Chinese (Simplified)}
%lang_subpkg -f zh-TW -p zh_TW -l %{quote:Chinese (Traditional)}
%endif


%prep
%autosetup -p1

%build
cd $RPM_BUILD_DIR/%source_prefix
kdehelperversion=$(cat toolkit/xre/nsKDEUtils.cpp | grep '#define KWATERFOXHELPER_VERSION' | cut -d ' ' -f 3)
if test "$kdehelperversion" != %{kde_helper_version}; then
  echo fix kde helper version in the .spec file
  exit 1
fi

export CC=clang
export CXX=clang++

cat >.mozconfig <<END
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
ac_add_options --disable-updater
ac_add_options --disable-verify-mar
ac_add_options --disable-profiling
ac_add_options --disable-signmar
ac_add_options --disable-tests

# Enable wanted features
ac_add_options --disable-stylo
ac_add_options --enable-release
ac_add_options --enable-rust-simd # on x86 requires SSE2
ac_add_options --enable-application=browser
ac_add_options --enable-eme=widevine
ac_add_options --enable-startup-notification
ac_add_options --enable-hardening

# System libraries
ac_add_options --with-system-zlib
# %if 0%{?suse_version} >= 1550 || 0%{?fedora}
# ac_add_options --with-system-nspr
# ac_add_options --with-system-nss
# %endif

export MOZ_GECKO_PROFILER=
export MOZ_ENABLE_PROFILER_SPS=
export MOZ_PROFILING=
export MOZ_INCLUDE_SOURCE_INFO=1
%if 0%{?suse_version} >= 1550
ac_add_options --disable-gconf
%endif
ac_add_options --disable-elf-hack
END

cp %{SOURCE3} $RPM_BUILD_DIR

export MOZ_SOURCE_CHANGESET=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export MOZ_SOURCE_REPO=https://github.com/WaterfoxCo/Waterfox-Classic

./mach build

%install
export MOZ_SOURCE_CHANGESET=$(awk -F ': ' '/^commit:/ {print $2; exit}' %{SOURCE7})
export MOZ_SOURCE_REPO=https://github.com/WaterfoxCo/Waterfox-Classic

cp %{SOURCE3} obj-x86_64-pc-linux-gnu/dist/bin/defaults/pref

DESTDIR=%{buildroot} ./mach install

%{__install} -Dm 644 %{SOURCE2} %{buildroot}%{progdir}/browser/defaults/preferences/vendor.js

%{__install} -Dm 644 %{SOURCE3} %{buildroot}%{progdir}/browser/defaults/preferences/kde.js

  for i in 16 22 24 32 48 64 128 256; do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    ln -Tsrf %{buildroot}%{progdir}/browser/chrome/icons/default/default$i.png \
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

  # Use system-provided dictionaries
  rm -rf "%{buildroot}%{progdir}/dictionaries"
  cat > %{buildroot}%{progdir}/browser/defaults/preferences/spellcheck.js <<END
pref("spellchecker.dictionary_path", "/usr/share/myspell");
END

  # Add syspref.js for setting preferences for all users
  %{__mkdir_p} %{buildroot}/etc/waterfox-classic
  %{__cp} %{SOURCE6} %{buildroot}/etc/waterfox-classic
  ln -Tsrf %{buildroot}/etc/waterfox-classic/syspref.js %{buildroot}%{progdir}/browser/defaults/preferences/syspref.js

  # Install a wrapper to avoid confusion about binary path
  %{__install} -Dm755 /dev/stdin "%{buildroot}/usr/bin/waterfox-classic" <<END
#!/bin/sh
exec %{progdir}/waterfox-classic "\$@"
END

  # Replace duplicate binary with wrapper
  # https://bugzilla.mozilla.org/show_bug.cgi?id=658850
  rm -rf "%{buildroot}%{progdir}/waterfox-classic-bin"
  ln -Tsrf "%{buildroot}/usr/bin/waterfox-classic" \
    "%{buildroot}%{progdir}/waterfox-classic-bin"

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
%dir /etc/%{progname}
%config /etc/%{progname}/syspref.js
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
%{_datadir}/appdata/
%dir %{_datadir}/icons/hicolor/384x384
%dir %{_datadir}/icons/hicolor/384x384/apps
%exclude %dir %{progdir}/browser/features
%exclude %{progdir}/browser/features

%changelog

%clean
rm -rf %{buildroot}

#
# spec file for package kwaterfoxhelper
#
#
# this is needed to match this package with the main package without the main package
# having a hard requirement on this package
%define helper_version 6
Name:           kwaterfoxhelper
Version:        5.0.6
Release:        0
Summary:        Integration of Waterfox with KDE Plasma
License:        MIT
Group:          System/GUI/KDE
URL:            https://github.com/hawkeye116477/kwaterfoxhelper
Source:         https://github.com/hawkeye116477/kwaterfoxhelper/archive/%{version}.tar.xz#/%{name}-%{version}.tar.xz
BuildRequires:  cmake
BuildRequires:  cmake(KF5I18n)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5Notifications)
BuildRequires:  cmake(KF5WindowSystem)
BuildRequires:  extra-cmake-modules
%if 0%{?is_opensuse}
BuildRequires:  ninja
%else
BuildRequires:	ninja-build
%endif
Requires:       waterfox-kde-version = %{helper_version}
%if 0%{?suse_version}
Supplements:    packageand(waterfox-classic-kpe:plasma5-desktop)
Supplements:    packageand(waterfox-g-kpe:plasma5-desktop)
%endif
%if 0%{?mageia} || 0%{?fedora} || 0%{?centos_version} != 700
Supplements:    packageand(waterfox-classic-kpe:plasma-desktop)
Supplements:    packageand(waterfox-g-kpe:plasma-desktop)
%endif
Conflicts:      waterfox-kde-version < %{helper_version}
%if 0%{?fedora} || 0%{?centos_version} != 700
%define debug_package %{nil}
%endif

%if 0%{?is_opensuse}
%define __builder ninja
%define __builddir %{_vpath_builddir}
%endif

%if 0%{?is_opensuse}
%define _vpath_builddir %_target_platform
%endif

%description
This is a helper application that allows Waterfox to use KDE file dialogs, file associations, protocol handlers and other KDE Plasma integration features.

%prep
%setup -q

%build
%if 0%{?centos} == 7
%undefine __cmake3_in_source_build
%endif
%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

version=$(grep '#define HELPER_VERSION' main.cpp | cut -d ' ' -f 3)
if test "$version" != %{helper_version}; then
    echo fix the version in the .spec file
    exit 1
fi
%if 0%{?centos_version} == 700
%{cmake3} \
%else
%{cmake} \
%endif
	-GNinja
%ninja_build \
%if !0%{?is_opensuse}
    -C %{_vpath_builddir}
%endif

%install
%ninja_install -C %{_vpath_builddir}

%files
%defattr(-,root,root)
%license LICENSE
%dir %{_prefix}/lib/waterfox
%{_prefix}/lib/waterfox/%{name}
%{_datadir}/knotifications5/kwaterfoxhelper.notifyrc

%changelog

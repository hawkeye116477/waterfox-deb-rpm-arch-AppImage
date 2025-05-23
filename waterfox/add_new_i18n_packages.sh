#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

sed -i '/Package: waterfox-i18n-/Q' $SCRIPT_PATH/control
mapfile -t _languages < <(cat $SCRIPT_PATH/locales.shipped)

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-i18n-$_locale_pkg
  _pkgname_trans3=waterfox-g3-i18n-$_locale_pkg
  _pkgname_trans4=waterfox-g4-i18n-$_locale_pkg
  _pkgname_trans5=waterfox-g-i18n-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname
Architecture: all
Depends: \${misc:Depends}, waterfox (>= \${source:Version})
Replaces: $_pkgname_trans4 (<< \${source:Version}), $_pkgname_trans3 (<< \${source:Version}), $_pkgname_trans5 (<< \${source:Version})
Breaks: $_pkgname_trans4 (<< \${source:Version}), $_pkgname_trans3 (<< \${source:Version}), $_pkgname_trans5 (<< \${source:Version})
Description: $_locale_desc language pack for Waterfox
 This package contains $_locale_desc translations for Waterfox

Package: $_pkgname_trans5
Architecture: all
Section: oldlibs
Depends: \${misc:Depends}, $_pkgname
Description: Transitional package
 This is a transitional package. It can safely be removed.

EOT
touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
extensions/langpack-${_locale_file}@l10n.waterfox.net.xpi /usr/lib/waterfox/browser/extensions
EOT
done

sed -i '$ d' $SCRIPT_PATH/control

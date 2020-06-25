#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

sed -i '/Package: waterfox-classic-i18n/Q' $SCRIPT_PATH/control
mapfile -t _languages < <(cat $SCRIPT_PATH/locales.shipped)

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-classic-i18n-$_locale_pkg
  _pkgname_trans=waterfox-locale-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname
Architecture: all
Depends: \${misc:Depends}, waterfox-classic-kpe (>= \${source:Version})
Replaces: $_pkgname_trans (<< \${source:Version})
Breaks: $_pkgname_trans (<< \${source:Version})
Description: $_locale_desc language pack for Waterfox Classic
 This package contains $_locale_desc translations for Waterfox Classic.

EOT

touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
features/langpack-${_locale_file}@waterfox.xpi /usr/lib/waterfox-classic/browser/features
EOT
done

sed -i '$ d' $SCRIPT_PATH/control

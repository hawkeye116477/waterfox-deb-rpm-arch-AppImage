#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

sed -i '/Package: waterfox-current-i18n-/Q' $SCRIPT_PATH/control
mapfile -t _languages < <(cat $SCRIPT_PATH/locales.shipped)

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-current-i18n-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname
Architecture: any
Depends: \${misc:Depends}, waterfox-current-kpe (>= \${source:Version})
Description: $_locale_desc language pack for Waterfox Current
 This package contains $_locale_desc translations for Waterfox Current

EOT
touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
debian/i18n/langpack-${_locale_file}@waterfox-current.xpi /usr/lib/waterfox-current/browser/extensions
EOT
done

sed -i '$ d' $SCRIPT_PATH/control

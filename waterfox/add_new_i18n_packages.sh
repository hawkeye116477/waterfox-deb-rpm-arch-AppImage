#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

sed -i '/Package: waterfox-locale/Q' $SCRIPT_PATH/control
mapfile -t _languages < <(cat $SCRIPT_PATH/locales.shipped)

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-locale-$_locale_file
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname
Architecture: any
Depends: \${misc:Depends}, waterfox  (>= \${source:Version})
Description: $_locale_desc language pack for Waterfox
 This package contains $_locale_desc translations for Waterfox

EOT
touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
features/langpack-${_locale_file}@waterfox.xpi /usr/lib/waterfox/browser/features
EOT
done

mapfile -t trans_languages < <(cat $SCRIPT_PATH/locales.transitional)

for trans_lang in "${trans_languages[@]}"; do
  trans_pkg=$(echo $trans_lang | awk -F: '{print $1}' | sed 's/^/waterfox-locale-/')
  depends=$(echo $trans_lang | awk -F: '{print $2}' | sed 's/^/waterfox-locale-/' | sed 's/,/, waterfox-locale-/g')

    cat <<EOT >> $SCRIPT_PATH/control
Package: $trans_pkg
Architecture: any
Depends: \${misc:Depends}, ${depends}
Description: Transitional package
 This is a transitional package. It can safely be removed.

EOT
done
sed -i '$ d' $SCRIPT_PATH/control

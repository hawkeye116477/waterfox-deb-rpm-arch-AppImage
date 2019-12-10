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
Architecture: any
Depends: \${misc:Depends}, waterfox-classic-kpe (>= \${source:Version})
Replaces: $_pkgname_trans (<< 2019.10-4)
Breaks: $_pkgname_trans (<< 2019.10-4)
Description: $_locale_desc language pack for Waterfox Classic
 This package contains $_locale_desc translations for Waterfox Classic.

EOT
done

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-classic-i18n-$_locale_pkg
  _pkgname_trans=waterfox-locale-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname_trans
Architecture: any
Section: oldlibs
Depends: \${misc:Depends}, $_pkgname
Description: Transitional package
 This is a transitional package. It can safely be removed.

EOT

touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
features/langpack-${_locale_file}@waterfox.xpi /usr/lib/waterfox-classic/browser/features
EOT
done

mapfile -t trans_languages < <(cat $SCRIPT_PATH/locales.transitional)

for trans_lang in "${trans_languages[@]}"; do
  trans_pkg=$(echo $trans_lang | awk -F: '{print $1}' | sed 's/^/waterfox-locale-/')
  depends=$(echo $trans_lang | awk -F: '{print $2}' | sed 's/^/waterfox-classic-i18n-/' | sed 's/,/, waterfox-classic-i18n-/g')

    cat <<EOT >> $SCRIPT_PATH/control
Package: $trans_pkg
Architecture: any
Section: oldlibs
Depends: \${misc:Depends}, ${depends}
Description: Transitional package
 This is a transitional package. It can safely be removed.

EOT
done
sed -i '$ d' $SCRIPT_PATH/control

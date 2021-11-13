#!/bin/bash

SCRIPT_PATH=$(dirname "$0")

sed -i '/Package: waterfox-g3-i18n-/Q' $SCRIPT_PATH/control
mapfile -t _languages < <(cat $SCRIPT_PATH/locales.shipped)

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-g3-i18n-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname
Architecture: all
Depends: \${misc:Depends}, waterfox-g3-kpe (>= \${source:Version})
Replaces: waterfox-current-i18n-$_locale_pkg (<< 2020.10-0)
Breaks: waterfox-current-i18n-$_locale_pkg (<< 2020.10-0)
Description: $_locale_desc language pack for Waterfox G3
 This package contains $_locale_desc translations for Waterfox G3

EOT
touch $SCRIPT_PATH/${_pkgname}.install

    cat <<EOT > $SCRIPT_PATH/${_pkgname}.install
extensions/langpack-${_locale_file}@l10n.waterfox.net.xpi /usr/lib/waterfox-g3/browser/extensions
EOT
done

for _lang in "${_languages[@]}"; do
  _locale_file=$(echo $_lang | awk -F: '{print $1}')
  _locale_pkg=$(echo $_lang | awk -F: '{print tolower($1)}')
  _locale_desc=$(echo $_lang | awk -F: '{print $2}')
  _pkgname=waterfox-g3-i18n-$_locale_pkg
  _pkgname_trans=waterfox-current-i18n-$_locale_pkg
    cat <<EOT >> $SCRIPT_PATH/control
Package: $_pkgname_trans
Architecture: all
Section: oldlibs
Depends: \${misc:Depends}, $_pkgname
Description: Transitional package
 This is a transitional package. It can safely be removed.

EOT
done

sed -i '$ d' $SCRIPT_PATH/control

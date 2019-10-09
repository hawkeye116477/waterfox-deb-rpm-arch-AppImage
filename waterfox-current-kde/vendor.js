// Disable default browser checking
pref("browser.shell.checkDefaultBrowser", false);

// Don't disable extensions dropped in to a system
// location, or those owned by the application
pref("extensions.autoDisableScopes", 3);

// Don't display the one-off addon selection dialog when
// upgrading from a version of Waterfox older than 8.0
pref("extensions.shownSelectionUI", true);

// Fall back to en-US search plugins if none exist for the current locale
pref("distribution.searchplugins.defaultLocale", "en-US");

// Use OS regional settings for date and time
pref("intl.regional_prefs.use_os_locales", true);

// Use system's dictionaries
pref("spellchecker.dictionary_path", "/usr/share/hunspell");

// Set update URL for extensions
pref("extensions.update.url", "https://versioncheck.addons.mozilla.org/update/VersionCheck.php?reqVersion=%REQ_VERSION%&id=%ITEM_ID%&version=%ITEM_VERSION%&maxAppVersion=%ITEM_MAXAPPVERSION%&status=%ITEM_STATUS%&appID=%APP_ID%&appVersion=%APP_VERSION%&appOS=%APP_OS%&appABI=%APP_ABI%&locale=%APP_LOCALE%&currentAppVersion=%CURRENT_APP_VERSION%&updateType=%UPDATE_TYPE%&compatMode=%COMPATIBILITY_MODE%");
pref("extensions.update.background.url", "https://versioncheck-bg.addons.mozilla.org/update/VersionCheck.php?reqVersion=%REQ_VERSION%&id=%ITEM_ID%&version=%ITEM_VERSION%&maxAppVersion=%ITEM_MAXAPPVERSION%&status=%ITEM_STATUS%&appID=%APP_ID%&appVersion=%APP_VERSION%&appOS=%APP_OS%&appABI=%APP_ABI%&locale=%APP_LOCALE%&currentAppVersion=%CURRENT_APP_VERSION%&updateType=%UPDATE_TYPE%&compatMode=%COMPATIBILITY_MODE%");

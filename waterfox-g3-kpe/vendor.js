// Disable default browser checking
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.defaultbrowser.notificationbar", false);

// Don't disable extensions in the application directory
pref("extensions.autoDisableScopes", 11);

// Don't display the one-off addon selection dialog when
// upgrading from a version of Waterfox older than 8.0
pref("extensions.shownSelectionUI", true);

// Fall back to en-US search plugins if none exist for the current locale
pref("distribution.searchplugins.defaultLocale", "en-US");

// Use OS regional settings for date and time
pref("intl.regional_prefs.use_os_locales", true);

// Use LANG environment variable to choose locale
pref("intl.locale.requested", "");

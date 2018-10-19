// Disable default browser checking
pref("browser.shell.checkDefaultBrowser", false);

// Don't disable extensions dropped in to a system
// location, or those owned by the application
pref("extensions.autoDisableScopes", 3);

// Don't display the one-off addon selection dialog when
// upgrading from a version of Waterfox older than 8.0
pref("extensions.shownSelectionUI", true);

//Disable automatic updates, because we have updates through repo, so this is not needed (updates aren't disabled for extensions)
pref("app.update.auto", false);
pref("app.update.enabled", false);

// Use LANG environment variable to choose locale
pref("intl.locale.matchOS", true);

// Fall back to en-US search plugins if none exist for the current locale
pref("distribution.searchplugins.defaultLocale", "en-US");

// Use OS regional settings for date and time
pref("intl.regional_prefs.use_os_locales", true);

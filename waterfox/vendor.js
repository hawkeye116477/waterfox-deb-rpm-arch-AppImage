// Disable default browser checking
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.defaultbrowser.notificationbar", false);

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

// Use LANG environment variable to choose locale
pref("intl.locale.requested", "");

// Enable Network Manager integration
pref("network.manage-offline-status", true);

// Disable downloading language packs, cuz Waterfox uses own and they are already included in subpackages
pref("extensions.getAddons.langpacks.url", "", locked);

// Disable requiring signatures for language packs
pref("extensions.langpacks.signatures.required", false, locked);

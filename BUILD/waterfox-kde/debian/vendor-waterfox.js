// Disable default browser checking
pref("browser.shell.checkDefaultBrowser", false);

// Don't disable extensions dropped in to a system
// location, or those owned by the application
pref("extensions.autoDisableScopes", 3);

// Don't display the one-off addon selection dialog when
// upgrading from a version of Waterfox older than 8.0
pref("extensions.shownSelectionUI", true);

// Disable e10s, because KDE patches are incompatible with e10s
pref("browser.tabs.remote.autostart", false);
pref("browser.tabs.remote.autostart.2", false);
pref("browser.tabs.remote.force-enable", false);

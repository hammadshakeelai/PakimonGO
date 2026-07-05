import 'package:shared_preferences/shared_preferences.dart';

import 'theme_controller.dart';

class SharedPrefsThemeStore implements ThemeStore {
  static const _key = 'theme_mode_v1';

  @override
  Future<String?> read() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_key);
  }

  @override
  Future<void> write(String value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, value);
  }
}

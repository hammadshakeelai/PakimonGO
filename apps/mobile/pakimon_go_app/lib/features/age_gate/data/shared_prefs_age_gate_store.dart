import 'package:shared_preferences/shared_preferences.dart';

import '../domain/age_gate_service.dart';

class SharedPrefsAgeGateStore implements AgeGateStore {
  static const _key = 'age_gate_v1';

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

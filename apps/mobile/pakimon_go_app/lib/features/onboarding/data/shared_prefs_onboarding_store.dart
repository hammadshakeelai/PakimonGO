import 'package:shared_preferences/shared_preferences.dart';

import '../domain/onboarding_service.dart';

class SharedPrefsOnboardingStore implements OnboardingStore {
  static const _key = 'onboarding_seen_v1';

  @override
  Future<bool> hasSeen() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_key) ?? false;
  }

  @override
  Future<void> markSeen() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_key, true);
  }
}

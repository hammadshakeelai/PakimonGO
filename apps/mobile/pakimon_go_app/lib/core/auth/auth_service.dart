import 'package:flutter/foundation.dart';

import '../network/api_config.dart';

class AuthService extends ChangeNotifier {
  String? _token;
  String? _userId;
  Future<String?> Function()? _tokenRefresher;

  String? get token => _token;
  String? get userId => _userId;
  bool get isAuthenticated => _token != null;

  String get effectiveToken => _token ?? ApiConfig.authToken;

  /// Returns a token that is valid *right now*. Firebase ID tokens expire
  /// after ~1 hour, so when a refresher is registered (Google sign-in) we
  /// ask the SDK for a fresh one — it returns its cache while still valid,
  /// so this is cheap to call on every request.
  Future<String> freshToken() async {
    final refresher = _tokenRefresher;
    if (refresher != null) {
      try {
        final refreshed = await refresher();
        if (refreshed != null && refreshed.isNotEmpty) {
          _token = refreshed;
          return refreshed;
        }
      } catch (_) {
        // Fall through to the last known token; the API will 401 and the
        // error UI takes over if it is truly no longer valid.
      }
    }
    return effectiveToken;
  }

  void loginWithUserId(String userId) {
    _userId = userId;
    _token = 'test_user_$userId';
    _tokenRefresher = null;
    notifyListeners();
  }

  void loginWithToken(String token, {Future<String?> Function()? refresher}) {
    _token = token;
    _userId = null;
    _tokenRefresher = refresher;
    notifyListeners();
  }

  void logout() {
    _token = null;
    _userId = null;
    _tokenRefresher = null;
    notifyListeners();
  }
}

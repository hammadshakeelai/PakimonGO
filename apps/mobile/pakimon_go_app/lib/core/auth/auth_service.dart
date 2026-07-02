import 'package:flutter/foundation.dart';

import '../network/api_config.dart';

class AuthService extends ChangeNotifier {
  String? _token;
  String? _userId;

  String? get token => _token;
  String? get userId => _userId;
  bool get isAuthenticated => _token != null;

  String get effectiveToken => _token ?? ApiConfig.authToken;

  void loginWithUserId(String userId) {
    _userId = userId;
    _token = 'test_user_$userId';
    notifyListeners();
  }

  void loginWithToken(String token) {
    _token = token;
    _userId = null;
    notifyListeners();
  }

  void logout() {
    _token = null;
    _userId = null;
    notifyListeners();
  }
}

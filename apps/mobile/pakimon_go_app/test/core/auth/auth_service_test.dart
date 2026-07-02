import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';

void main() {
  group('AuthService', () {
    test('starts unauthenticated', () {
      final auth = AuthService();
      expect(auth.isAuthenticated, isFalse);
      expect(auth.token, isNull);
      expect(auth.userId, isNull);
    });

    test('loginWithUserId sets token and userId', () {
      final auth = AuthService();
      auth.loginWithUserId('bob');
      expect(auth.isAuthenticated, isTrue);
      expect(auth.token, 'test_user_bob');
      expect(auth.userId, 'bob');
    });

    test('loginWithToken sets token only', () {
      final auth = AuthService();
      auth.loginWithToken('custom_token_123');
      expect(auth.isAuthenticated, isTrue);
      expect(auth.token, 'custom_token_123');
      expect(auth.userId, isNull);
    });

    test('logout clears state', () {
      final auth = AuthService();
      auth.loginWithUserId('alice');
      expect(auth.isAuthenticated, isTrue);

      auth.logout();
      expect(auth.isAuthenticated, isFalse);
      expect(auth.token, isNull);
      expect(auth.userId, isNull);
    });

    test('effectiveToken returns login token when set', () {
      final auth = AuthService();
      auth.loginWithToken('my_token');
      expect(auth.effectiveToken, 'my_token');
    });

    test('effectiveToken returns default when not logged in', () {
      final auth = AuthService();
      expect(auth.effectiveToken, isNotNull);
      expect(auth.effectiveToken.length, greaterThan(0));
    });

    test('notifies listeners on login', () {
      final auth = AuthService();
      int calls = 0;
      auth.addListener(() => calls++);

      auth.loginWithUserId('charlie');
      expect(calls, 1);
    });

    test('notifies listeners on logout', () {
      final auth = AuthService();
      auth.loginWithUserId('dave');
      int calls = 0;
      auth.addListener(() => calls++);

      auth.logout();
      expect(calls, 1);
    });
  });
}

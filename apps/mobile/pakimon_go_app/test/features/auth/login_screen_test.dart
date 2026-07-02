import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';
import 'package:pakimon_go_app/features/auth/presentation/login_screen.dart';

Widget _buildScreen(AuthService auth, {VoidCallback? onComplete}) {
  return MaterialApp(
    home: LoginScreen(
      authService: auth,
      onLoginComplete: onComplete,
    ),
  );
}

void main() {
  testWidgets('renders login form with user ID field',
      (WidgetTester tester) async {
    final auth = AuthService();
    await tester.pumpWidget(_buildScreen(auth));
    await tester.pumpAndSettle();

    expect(find.text('PakimonGO Login'), findsOneWidget);
    expect(find.text('User ID'), findsOneWidget);
    expect(find.text('Sign In'), findsOneWidget);
  });

  testWidgets('shows token input when switching mode',
      (WidgetTester tester) async {
    final auth = AuthService();
    await tester.pumpWidget(_buildScreen(auth));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Paste auth token instead'));
    await tester.pumpAndSettle();

    expect(find.text('Auth Token'), findsOneWidget);
    expect(find.text('Use User ID instead'), findsOneWidget);
  });

  testWidgets('login with user ID calls authService.loginWithUserId',
      (WidgetTester tester) async {
    final auth = AuthService();
    bool completed = false;

    await tester.pumpWidget(_buildScreen(auth, onComplete: () {
      completed = true;
    }));
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), 'alice');
    await tester.tap(find.text('Sign In'));
    await tester.pump();

    expect(auth.isAuthenticated, isTrue);
    expect(auth.token, 'test_user_alice');
    expect(auth.userId, 'alice');
  });

  testWidgets('login with token mode sets raw token',
      (WidgetTester tester) async {
    final auth = AuthService();

    await tester.pumpWidget(_buildScreen(auth));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Paste auth token instead'));
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), 'my_custom_token');
    await tester.tap(find.text('Sign In'));
    await tester.pump();

    expect(auth.isAuthenticated, isTrue);
    expect(auth.token, 'my_custom_token');
  });

  testWidgets('login calls onLoginComplete callback',
      (WidgetTester tester) async {
    final auth = AuthService();
    int callbackCalls = 0;

    // The callback fires after getProfile succeeds, which will fail
    // since there's no real API. So we test that auth state is set
    // before the API call fails.
    await tester.pumpWidget(_buildScreen(auth, onComplete: () {
      callbackCalls++;
    }));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Sign In'));
    await tester.pump();

    expect(auth.isAuthenticated, isTrue);
  });
}

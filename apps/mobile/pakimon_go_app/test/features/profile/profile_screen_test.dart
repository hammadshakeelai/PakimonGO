import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/profile/domain/profile_viewmodel.dart';
import 'package:pakimon_go_app/features/profile/presentation/profile_screen.dart';

import 'package:http/http.dart' as http;
import 'dart:convert';

class _MockClient extends http.BaseClient {
  final Map<String, http.Response> responses;

  _MockClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url}';
    final resp = responses[key];
    if (resp != null) {
      return http.StreamedResponse(
        http.ByteStream.fromBytes(resp.bodyBytes),
        resp.statusCode,
        headers: resp.headers,
      );
    }
    return http.StreamedResponse(
      http.ByteStream.fromBytes(utf8.encode('{"detail": "not found"}')),
      404,
    );
  }
}

Map<String, dynamic> _profileJson({String? ageBand, String? homeRegion}) => {
      'userId': 'user-123',
      'email': 'test@example.com',
      'status': 'active',
      'ageBand': ageBand,
      'homeRegion': homeRegion,
      'trustState': 'basic',
      'createdAt': '2026-07-03T00:00:00',
    };

void main() {
  group('ProfileScreen', () {
    testWidgets('shows loading indicator initially', (tester) async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(
          viewModel: vm,
          authService: AuthService(),
        ),
      ));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows profile info after loading', (tester) async {
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: 'teen', homeRegion: 'Punjab')),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(
          viewModel: vm,
          authService: AuthService(),
        ),
      ));
      await tester.pumpAndSettle();
      expect(find.text('user-123'), findsOneWidget);
      expect(find.text('test@example.com'), findsOneWidget);
    });

    testWidgets('renders when backend holds an age band outside the presets',
        (tester) async {
      // Regression: seed users carry legacy bands like "18_24"; an unknown
      // dropdown value used to crash the whole Profile screen.
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: '18_24', homeRegion: 'PK')),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(
          viewModel: vm,
          authService: AuthService(),
        ),
      ));
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.text('user-123'), findsOneWidget);
      expect(find.text('18_24'), findsOneWidget);
    });

    testWidgets('shows error state with retry button', (tester) async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(
          viewModel: vm,
          authService: AuthService(),
        ),
      ));
      await tester.pumpAndSettle();
      expect(find.textContaining('Retry'), findsOneWidget);
    });

    testWidgets('Delete My Account opens a confirm dialog, cancel keeps the account',
        (tester) async {
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: 'teen', homeRegion: 'Punjab')),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      final auth = AuthService()..loginWithUserId('alice');
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(viewModel: vm, authService: auth),
      ));
      await tester.pumpAndSettle();

      await tester.dragUntilVisible(
        find.byKey(const Key('delete_account_button')),
        find.byType(ListView),
        const Offset(0, -100),
      );
      await tester.tap(find.byKey(const Key('delete_account_button')));
      await tester.pumpAndSettle();
      expect(find.text('Delete your account?'), findsOneWidget);

      await tester.tap(find.text('Cancel'));
      await tester.pumpAndSettle();
      expect(auth.isAuthenticated, isTrue);
    });

    testWidgets('Confirming deletion calls the API and logs the user out',
        (tester) async {
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: 'teen', homeRegion: 'Punjab')),
          200,
          headers: {'content-type': 'application/json'},
        ),
        'DELETE http://test.com/users/me': http.Response('', 204),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      final auth = AuthService()..loginWithUserId('alice');
      await tester.pumpWidget(MaterialApp(
        home: ProfileScreen(viewModel: vm, authService: auth),
      ));
      await tester.pumpAndSettle();

      await tester.dragUntilVisible(
        find.byKey(const Key('delete_account_button')),
        find.byType(ListView),
        const Offset(0, -100),
      );
      await tester.tap(find.byKey(const Key('delete_account_button')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Delete'));
      await tester.pumpAndSettle();

      expect(auth.isAuthenticated, isFalse);
    });
  });
}

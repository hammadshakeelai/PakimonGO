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
  group('ProfileViewModel', () {
    test('starts in loading state', () {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      expect(vm.state, ProfileLoadState.loading);
    });

    test('fetchProfile loads profile', () async {
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
      await vm.fetchProfile();

      expect(vm.state, ProfileLoadState.loaded);
      expect(vm.profile, isNotNull);
      expect(vm.profile!.userId, 'user-123');
      expect(vm.selectedAgeBand, 'teen');
      expect(vm.homeRegion, 'Punjab');
    });

    test('fetchProfile handles error', () async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await vm.fetchProfile();

      expect(vm.state, ProfileLoadState.error);
      expect(vm.error, isNotNull);
    });

    test('setAgeBand updates age band', () {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      vm.setAgeBand('adult');
      expect(vm.selectedAgeBand, 'adult');
    });

    test('setHomeRegion updates home region', () {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      vm.setHomeRegion('Sindh');
      expect(vm.homeRegion, 'Sindh');
    });

    test('hasChanges detects changes', () async {
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
      await vm.fetchProfile();

      expect(vm.hasChanges, false);
      vm.setAgeBand('adult');
      expect(vm.hasChanges, true);
    });

    test('saveProfile sends PATCH and updates profile', () async {
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: 'teen', homeRegion: 'Punjab')),
          200,
          headers: {'content-type': 'application/json'},
        ),
        'PATCH http://test.com/users/me': http.Response(
          jsonEncode(
              _profileJson(ageBand: 'adult', homeRegion: 'Punjab')),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await vm.fetchProfile();

      vm.setAgeBand('adult');
      final success = await vm.saveProfile();
      expect(success, true);
      expect(vm.profile!.ageBand, 'adult');
    });

    test('saveProfile handles error', () async {
      final client = _MockClient({
        'GET http://test.com/users/me': http.Response(
          jsonEncode(_profileJson(ageBand: 'teen')),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);
      await vm.fetchProfile();

      vm.setAgeBand('adult');
      final success = await vm.saveProfile();
      expect(success, false);
      expect(vm.saveError, isNotNull);
    });
  });

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
  });
}

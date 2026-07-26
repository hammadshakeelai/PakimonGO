import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/profile/domain/profile_viewmodel.dart';

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

    test('deleteAccount calls DELETE /users/me and reports success',
        () async {
      final client = _MockClient({
        'DELETE http://test.com/users/me': http.Response('', 204),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);

      final success = await vm.deleteAccount();
      expect(success, true);
      expect(vm.isDeleting, false);
      expect(vm.deleteError, isNull);
    });

    test('deleteAccount surfaces the backend error on failure', () async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = ProfileViewModel(repository: repo);

      final success = await vm.deleteAccount();
      expect(success, false);
      expect(vm.deleteError, isNotNull);
    });
  });
}

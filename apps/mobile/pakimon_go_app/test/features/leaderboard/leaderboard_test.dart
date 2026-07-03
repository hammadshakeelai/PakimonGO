import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/leaderboard/domain/leaderboard_viewmodel.dart';
import 'package:pakimon_go_app/features/leaderboard/presentation/leaderboard_screen.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class _MockClient extends http.BaseClient {
  final Map<String, http.StreamedResponse> responses;

  _MockClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url.path}';
    final resp = responses[key];
    if (resp != null) return resp;
    return http.StreamedResponse(
      Stream.value(utf8.encode('{"error":"not found"}')),
      404,
    );
  }
}

ApiClient _makeClient(Map<String, http.StreamedResponse> responses) {
  return ApiClient(baseUrl: 'http://test', client: _MockClient(responses));
}

http.StreamedResponse _jsonResponse(int status, Map<String, dynamic> body) {
  return http.StreamedResponse(
    Stream.value(utf8.encode(jsonEncode(body))),
    status,
    headers: {'content-type': 'application/json'},
  );
}

void main() {
  group('LeaderboardEntry', () {
    test('fromJson parses correctly', () {
      final entry = LeaderboardEntry.fromJson({
        'userId': 'u1',
        'ageBand': 'adult',
        'homeRegion': 'PK',
        'totalScore': 150,
        'submissionCount': 7,
      });
      expect(entry.userId, 'u1');
      expect(entry.totalScore, 150);
      expect(entry.submissionCount, 7);
    });

    test('fromJson handles nulls', () {
      final entry = LeaderboardEntry.fromJson({
        'userId': 'u2',
        'totalScore': null,
        'submissionCount': null,
      });
      expect(entry.totalScore, 0);
      expect(entry.submissionCount, 0);
    });
  });

  group('LeaderboardViewModel', () {
    test('starts empty', () {
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: ApiClient()),
      );
      expect(vm.entries, isEmpty);
      expect(vm.isLoading, false);
      expect(vm.error, isNull);
    });

    test('fetchLeaderboard populates entries', () async {
      final client = _makeClient({
        'GET /leaderboard': _jsonResponse(200, {
          'entries': [
            {
              'userId': 'u1',
              'totalScore': 100,
              'submissionCount': 5,
            },
            {
              'userId': 'u2',
              'totalScore': 50,
              'submissionCount': 3,
            },
          ],
          'pagination': {'total': 2, 'limit': 50, 'offset': 0},
        }),
      });
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: client),
      );

      await vm.fetchLeaderboard();

      expect(vm.entries.length, 2);
      expect(vm.entries[0].userId, 'u1');
      expect(vm.entries[0].totalScore, 100);
      expect(vm.error, isNull);
    });

    test('fetchLeaderboard handles error', () async {
      final client = _makeClient({
        'GET /leaderboard': _jsonResponse(500, {'error': 'fail'}),
      });
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: client),
      );

      await vm.fetchLeaderboard();

      expect(vm.entries, isEmpty);
      expect(vm.error, isNotNull);
    });
  });

  group('LeaderboardScreen', () {
    Widget _buildTestApp(LeaderboardViewModel vm) {
      return MaterialApp(
        home: Scaffold(body: LeaderboardScreen(viewModel: vm)),
      );
    }

    testWidgets('shows loading indicator', (WidgetTester tester) async {
      final client = _makeClient({
        'GET /leaderboard': _jsonResponse(200, {'entries': [], 'pagination': {}}),
      });
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: client),
      );
      vm.fetchLeaderboard();
      await tester.pumpWidget(_buildTestApp(vm));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows empty state', (WidgetTester tester) async {
      final client = _makeClient({
        'GET /leaderboard': _jsonResponse(200, {'entries': [], 'pagination': {}}),
      });
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: client),
      );
      await tester.pumpWidget(_buildTestApp(vm));
      await tester.pump();
      await tester.pump(const Duration(seconds: 1));
      expect(find.text('No leaderboard data yet'), findsOneWidget);
    });

    testWidgets('shows entries with scores', (WidgetTester tester) async {
      final client = _makeClient({
        'GET /leaderboard': _jsonResponse(200, {
          'entries': [
            {'userId': 'alice', 'totalScore': 200, 'submissionCount': 10},
            {'userId': 'bob', 'totalScore': 100, 'submissionCount': 5},
          ],
          'pagination': {'total': 2, 'limit': 50, 'offset': 0},
        }),
      });
      final vm = LeaderboardViewModel(
        repository: CaptureRepository(client: client),
      );
      await tester.pumpWidget(_buildTestApp(vm));
      await tester.pump();
      await tester.pump(const Duration(seconds: 1));

      expect(find.text('alice'), findsOneWidget);
      expect(find.text('bob'), findsOneWidget);
      expect(find.text('200 pts'), findsOneWidget);
      expect(find.text('100 pts'), findsOneWidget);
    });
  });
}

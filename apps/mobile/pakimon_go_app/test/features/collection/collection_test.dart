import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';
import 'package:pakimon_go_app/features/collection/presentation/collection_screen.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

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

Map<String, dynamic> _collectionJson() => {
      'userId': 'user-123',
      'species': [
        {
          'species': 'Markhor',
          'context': 'wild',
          'totalPoints': 75,
          'captureCount': 3,
          'lastCaptured': '2026-07-03T10:00:00',
        },
        {
          'species': 'Peacock',
          'context': 'zoo',
          'totalPoints': 5,
          'captureCount': 5,
          'lastCaptured': '2026-07-02T10:00:00',
        },
      ],
      'pagination': {'limit': 20, 'offset': 0, 'total': 2},
    };

void main() {
  group('CollectionViewModel', () {
    test('starts in loading state', () {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      expect(vm.state, CollectionLoadState.loading);
    });

    test('fetchCollection loads species', () async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.loaded);
      expect(vm.entries.length, 2);
      expect(vm.entries[0].species, 'Markhor');
      expect(vm.entries[1].species, 'Peacock');
      expect(vm.total, 2);
    });

    test('fetchCollection handles error', () async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.error);
      expect(vm.error, isNotNull);
    });

    test('fetchCollection shows empty state', () async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode({
            'userId': 'user-123',
            'species': [],
            'pagination': {'limit': 20, 'offset': 0, 'total': 0},
          }),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.empty);
    });

    test('setSortBy re-fetches', () async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=species&sort_order=desc':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await vm.fetchCollection();

      vm.setSortBy('species');
      expect(vm.sortBy, 'species');
    });

    test('setContextFilter re-fetches', () async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc&context=wild':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await vm.fetchCollection();

      vm.setContextFilter('wild');
      expect(vm.contextFilter, 'wild');
    });
  });

  group('CollectionScreen', () {
    testWidgets('shows loading indicator initially', (tester) async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(body: CollectionScreen(viewModel: vm)),
      ));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows species list after loading', (tester) async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode(_collectionJson()),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(body: CollectionScreen(viewModel: vm)),
      ));
      await tester.pumpAndSettle();
      expect(find.text('Markhor'), findsOneWidget);
      expect(find.text('Peacock'), findsOneWidget);
    });

    testWidgets('shows empty state', (tester) async {
      final client = _MockClient({
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc':
            http.Response(
          jsonEncode({
            'userId': 'user-123',
            'species': [],
            'pagination': {'limit': 20, 'offset': 0, 'total': 0},
          }),
          200,
          headers: {'content-type': 'application/json'},
        ),
      });
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(body: CollectionScreen(viewModel: vm)),
      ));
      await tester.pumpAndSettle();
      expect(find.text('No species collected yet'), findsOneWidget);
    });

    testWidgets('shows error state with retry', (tester) async {
      final client = _MockClient({});
      final repo = CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      );
      final vm = CollectionViewModel(repository: repo);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(body: CollectionScreen(viewModel: vm)),
      ));
      await tester.pumpAndSettle();
      expect(find.textContaining('Retry'), findsOneWidget);
    });
  });
}

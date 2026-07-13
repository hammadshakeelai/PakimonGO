import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';
import 'package:pakimon_go_app/features/collection/presentation/collection_screen.dart';

import 'collection_test_helpers.dart';

CollectionViewModel _vm(MockCollectionClient client) => CollectionViewModel(
    repository: CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com')));

http.Response _ok(Map<String, dynamic> body) => http.Response(
    jsonEncode(body), 200,
    headers: {'content-type': 'application/json'});

const _listUrl =
    'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc';

void main() {
  group('CollectionScreen', () {
    testWidgets('shows loading indicator initially', (tester) async {
      final vm = _vm(MockCollectionClient({}));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows species list after loading', (tester) async {
      final vm = _vm(MockCollectionClient({_listUrl: _ok(collectionJson())}));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      await tester.pumpAndSettle();
      expect(find.text('Markhor'), findsOneWidget);
      expect(find.text('Peacock'), findsOneWidget);
    });

    testWidgets('shows empty state', (tester) async {
      final vm = _vm(MockCollectionClient({
        _listUrl: _ok({
          'userId': 'user-123',
          'species': [],
          'pagination': {'limit': 20, 'offset': 0, 'total': 0},
        }),
      }));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      await tester.pumpAndSettle();
      expect(find.text('No species collected yet'), findsOneWidget);
    });

    testWidgets('shows error state with retry', (tester) async {
      final vm = _vm(MockCollectionClient({}));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      await tester.pumpAndSettle();
      expect(find.textContaining('Retry'), findsOneWidget);
    });

    testWidgets('tapping species navigates to SpeciesDetailScreen',
        (tester) async {
      final vm = _vm(MockCollectionClient({_listUrl: _ok(collectionJson())}));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Markhor'));
      await tester.pumpAndSettle();
      expect(find.text('Markhor'), findsAtLeast(1));
      // Regression: the detail marker now carries the representative
      // submission's coarse cell location instead of 0.0000.
      expect(find.text('33.6800'), findsOneWidget);
      expect(find.text('73.0500'), findsOneWidget);
      expect(find.text('Photo not available'), findsNothing);
    });

    testWidgets(
        'entry without representative photo/location degrades gracefully',
        (tester) async {
      final vm = _vm(MockCollectionClient({_listUrl: _ok(collectionJson())}));
      await tester.pumpWidget(MaterialApp(
        home: CollectionScreen(viewModel: vm),
      ));
      await tester.pumpAndSettle();

      // Peacock has null mediaAssetId + publicLocation in the fixture.
      await tester.tap(find.text('Peacock'));
      await tester.pumpAndSettle();
      expect(find.text('Photo not available'), findsNothing);
      expect(find.textContaining('Latitude'), findsNothing);
      expect(find.text('Hidden for privacy'), findsOneWidget);
    });
  });
}

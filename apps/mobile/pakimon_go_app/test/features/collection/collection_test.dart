import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';

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
  group('CollectionViewModel', () {
    test('starts in loading state', () {
      final vm = _vm(MockCollectionClient({}));
      expect(vm.state, CollectionLoadState.loading);
    });

    test('fetchCollection loads species', () async {
      final vm = _vm(MockCollectionClient({_listUrl: _ok(collectionJson())}));
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.loaded);
      expect(vm.entries.length, 2);
      expect(vm.entries[0].species, 'Markhor');
      expect(vm.entries[1].species, 'Peacock');
      expect(vm.total, 2);
    });

    test('fetchCollection handles error', () async {
      final vm = _vm(MockCollectionClient({}));
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.error);
      expect(vm.error, isNotNull);
    });

    test('fetchCollection shows empty state', () async {
      final vm = _vm(MockCollectionClient({
        _listUrl: _ok({
          'userId': 'user-123',
          'species': [],
          'pagination': {'limit': 20, 'offset': 0, 'total': 0},
        }),
      }));
      await vm.fetchCollection();

      expect(vm.state, CollectionLoadState.empty);
    });

    test('setSortBy re-fetches', () async {
      final vm = _vm(MockCollectionClient({
        _listUrl: _ok(collectionJson()),
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=species&sort_order=desc':
            _ok(collectionJson()),
      }));
      await vm.fetchCollection();

      vm.setSortBy('species');
      expect(vm.sortBy, 'species');
    });

    test('setContextFilter re-fetches', () async {
      final vm = _vm(MockCollectionClient({
        _listUrl: _ok(collectionJson()),
        'GET http://test.com/users/me/collection?limit=20&offset=0&sort_by=totalPoints&sort_order=desc&context=wild':
            _ok(collectionJson()),
      }));
      await vm.fetchCollection();

      vm.setContextFilter('wild');
      expect(vm.contextFilter, 'wild');
    });
  });
}

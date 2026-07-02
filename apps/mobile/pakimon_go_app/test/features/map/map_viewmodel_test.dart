import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/map/domain/map_viewmodel.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class _MockHttpClient extends http.BaseClient {
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    throw UnimplementedError('not used in test');
  }
}

class _MockRepository extends CaptureRepository {
  final List<SubmissionMarker>? markers;
  final Exception? error;

  _MockRepository({this.markers, this.error})
      : super(
          client: ApiClient(
            client: _MockHttpClient(),
            baseUrl: 'http://test/api',
            tokenProvider: () => 'test',
          ),
        );

  @override
  Future<List<SubmissionMarker>> getMapMarkers({int limit = 200}) {
    if (error != null) throw error!;
    return Future.value(markers ?? []);
  }
}

void main() {
  group('MapViewModel', () {
    test('starts with empty markers', () {
      final vm = MapViewModel(repository: _MockRepository());
      expect(vm.markers, isEmpty);
      expect(vm.isLoading, false);
      expect(vm.error, isNull);
      expect(vm.markerCount, 0);
      expect(vm.hasMarkers, false);
    });

    test('fetchMarkers populates markers on success', () async {
      final markers = [
        SubmissionMarker(
          submissionId: 's1',
          mediaAssetId: 'm1',
          latitude: 51.5,
          longitude: -0.12,
          species: 'Passer domesticus',
          points: 25,
          status: 'scored',
        ),
        SubmissionMarker(
          submissionId: 's2',
          mediaAssetId: 'm2',
          latitude: 48.85,
          longitude: 2.35,
          species: 'Felis catus',
          points: 1,
          status: 'capped',
        ),
      ];
      final vm = MapViewModel(repository: _MockRepository(markers: markers));

      await vm.fetchMarkers();

      expect(vm.markers, hasLength(2));
      expect(vm.markerCount, 2);
      expect(vm.hasMarkers, true);
      expect(vm.error, isNull);
      expect(vm.isLoading, false);
      expect(vm.markers[0].species, 'Passer domesticus');
      expect(vm.markers[1].submissionId, 's2');
    });

    test('fetchMarkers handles error', () async {
      final vm = MapViewModel(
        repository: _MockRepository(error: Exception('API error')),
      );

      await vm.fetchMarkers();

      expect(vm.markers, isEmpty);
      expect(vm.hasMarkers, false);
      expect(vm.error, contains('API error'));
      expect(vm.isLoading, false);
    });

    test('notifies listeners on fetch start and end', () async {
      final vm = MapViewModel(repository: _MockRepository(markers: []));
      int notifyCount = 0;
      vm.addListener(() => notifyCount++);

      await vm.fetchMarkers();

      expect(notifyCount, 2);
    });

    test('clusters are empty for 3 or fewer markers', () async {
      final vm = MapViewModel(
        repository: _MockRepository(
          markers: [
            SubmissionMarker(
                submissionId: 's1',
                mediaAssetId: 'm1',
                latitude: 51.5,
                longitude: -0.12,
                species: 'A',
                points: 1,
                status: 'scored'),
            SubmissionMarker(
                submissionId: 's2',
                mediaAssetId: 'm2',
                latitude: 52.0,
                longitude: -0.12,
                species: 'B',
                points: 1,
                status: 'scored'),
          ],
        ),
      );

      await vm.fetchMarkers();

      expect(vm.clusters, isEmpty);
      expect(vm.clusterCount, 0);
    });

    test('clusters generated for more than 3 markers', () async {
      final vm = MapViewModel(
        repository: _MockRepository(
          markers: [
            SubmissionMarker(
                submissionId: 's1',
                mediaAssetId: 'm1',
                latitude: 51.5,
                longitude: -0.12,
                species: 'Passer domesticus',
                points: 25,
                status: 'scored'),
            SubmissionMarker(
                submissionId: 's2',
                mediaAssetId: 'm2',
                latitude: 51.501,
                longitude: -0.121,
                species: 'Passer domesticus',
                points: 25,
                status: 'scored'),
            SubmissionMarker(
                submissionId: 's3',
                mediaAssetId: 'm3',
                latitude: 51.502,
                longitude: -0.122,
                species: 'Felis catus',
                points: 1,
                status: 'capped'),
            SubmissionMarker(
                submissionId: 's4',
                mediaAssetId: 'm4',
                latitude: 52.0,
                longitude: 2.0,
                species: 'Canis lupus',
                points: 25,
                status: 'scored'),
          ],
        ),
      );

      await vm.fetchMarkers();

      expect(vm.clusterCount, greaterThan(0));
      expect(vm.markerCount, 4);
    });
  });
}

import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/map/domain/cluster_service.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

SubmissionMarker _m(String id, double lat, double lng, String species) {
  return SubmissionMarker(
    submissionId: id,
    mediaAssetId: id,
    latitude: lat,
    longitude: lng,
    species: species,
    points: 25,
    status: 'scored',
  );
}

void main() {
  group('ClusterService', () {
    test('returns empty for empty markers', () {
      final result = ClusterService.cluster([]);
      expect(result, isEmpty);
    });

    test('groups nearby markers into one cluster', () {
      final markers = [
        _m('s1', 51.5, -0.12, 'Passer domesticus'),
        _m('s2', 51.501, -0.121, 'Passer domesticus'),
        _m('s3', 51.502, -0.122, 'Felis catus'),
      ];
      final result = ClusterService.cluster(markers);
      expect(result.length, 1);
      expect(result.first.count, 3);
      expect(result.first.isCluster, true);
    });

    test('separates distant markers into different clusters', () {
      final markers = [
        _m('s1', 51.5, -0.12, 'Passer domesticus'),
        _m('s2', 52.5, -0.12, 'Felis catus'),
      ];
      final result = ClusterService.cluster(markers);
      expect(result.length, 2);
      expect(result[0].count, 1);
      expect(result[1].count, 1);
      expect(result[0].isCluster, false);
    });

    test('speciesPreview shows up to 2 species with overflow count', () {
      final cluster = ClusterMarker(
        latitude: 51.5,
        longitude: -0.12,
        count: 5,
        species: ['Canis lupus', 'Felis catus', 'Passer domesticus'],
      );

      expect(cluster.speciesPreview, 'Canis lupus, Felis catus +1');
    });

    test('speciesPreview with empty species returns Unknown', () {
      final cluster = ClusterMarker(
        latitude: 51.5,
        longitude: -0.12,
        count: 1,
        species: [],
      );

      expect(cluster.speciesPreview, 'Unknown');
    });

    test('speciesPreview with one species returns it directly', () {
      final cluster = ClusterMarker(
        latitude: 51.5,
        longitude: -0.12,
        count: 3,
        species: ['Passer domesticus'],
      );

      expect(cluster.speciesPreview, 'Passer domesticus');
    });
  });
}

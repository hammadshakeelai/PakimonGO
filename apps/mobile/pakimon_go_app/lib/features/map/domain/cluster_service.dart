import 'dart:math';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class ClusterMarker {
  final double latitude;
  final double longitude;
  final int count;
  final List<String> species;

  ClusterMarker({
    required this.latitude,
    required this.longitude,
    required this.count,
    required this.species,
  });

  String get speciesPreview {
    if (species.isEmpty) return 'Unknown';
    if (species.length <= 2) return species.join(', ');
    return '${species.take(2).join(', ')} +${species.length - 2}';
  }

  bool get isCluster => count > 1;
}

class ClusterService {
  static double _toRadians(double deg) => deg * pi / 180;

  static double _haversineKm(
      double lat1, double lon1, double lat2, double lon2) {
    const r = 6371.0;
    final dLat = _toRadians(lat2 - lat1);
    final dLon = _toRadians(lon2 - lon1);
    final a = sin(dLat / 2) * sin(dLat / 2) +
        cos(_toRadians(lat1)) *
            cos(_toRadians(lat2)) *
            sin(dLon / 2) *
            sin(dLon / 2);
    return r * 2 * atan2(sqrt(a), sqrt(1 - a));
  }

  static List<ClusterMarker> cluster(
      List<SubmissionMarker> markers, {double maxDistanceKm = 2.0}) {
    if (markers.isEmpty) return [];

    final assigned = List.filled(markers.length, -1);
    final clusters = <ClusterMarker>[];
    var clusterIndex = 0;

    for (var i = 0; i < markers.length; i++) {
      if (assigned[i] != -1) continue;

      final members = <SubmissionMarker>[markers[i]];
      assigned[i] = clusterIndex;

      for (var j = i + 1; j < markers.length; j++) {
        if (assigned[j] != -1) continue;

        final dist = _haversineKm(
          markers[i].latitude, markers[i].longitude,
          markers[j].latitude, markers[j].longitude,
        );

        if (dist <= maxDistanceKm) {
          members.add(markers[j]);
          assigned[j] = clusterIndex;
        }
      }

      final avgLat =
          members.fold(0.0, (s, m) => s + m.latitude) / members.length;
      final avgLng =
          members.fold(0.0, (s, m) => s + m.longitude) / members.length;
      final species =
          {for (final m in members) m.species}.toList()..sort();

      clusters.add(ClusterMarker(
        latitude: avgLat,
        longitude: avgLng,
        count: members.length,
        species: species,
      ));

      clusterIndex++;
    }

    return clusters;
  }
}

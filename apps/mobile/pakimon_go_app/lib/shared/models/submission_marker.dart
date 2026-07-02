class SubmissionMarker {
  final String submissionId;
  final double latitude;
  final double longitude;
  final String species;
  final int points;
  final String status;

  SubmissionMarker({
    required this.submissionId,
    required this.latitude,
    required this.longitude,
    required this.species,
    required this.points,
    required this.status,
  });

  factory SubmissionMarker.fromJson(Map<String, dynamic> json) {
    final loc = json['publicLocation'] as Map<String, dynamic>? ?? {};
    return SubmissionMarker(
      submissionId: json['submissionId'] as String,
      latitude: (loc['cellLatitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (loc['cellLongitude'] as num?)?.toDouble() ?? 0.0,
      species: json['realName'] as String? ?? 'Unknown',
      points: (json['scoreState'] is Map
              ? (json['scoreState'] as Map)['visiblePoints']
              : null)
          as int? ?? 0,
      status: (json['scoreState'] is Map
              ? (json['scoreState'] as Map)['status']
              : null)
          as String? ?? 'pending',
    );
  }

  bool get hasValidLocation => latitude != 0.0 || longitude != 0.0;
}

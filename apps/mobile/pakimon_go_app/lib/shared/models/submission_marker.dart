class SubmissionMarker {
  final String submissionId;
  final String mediaAssetId;
  final double latitude;
  final double longitude;
  final String species;
  final int points;
  final String status;

  SubmissionMarker({
    required this.submissionId,
    required this.mediaAssetId,
    required this.latitude,
    required this.longitude,
    required this.species,
    required this.points,
    required this.status,
  });

  factory SubmissionMarker.fromJson(Map<String, dynamic> json) {
    // Handles both payload shapes: the detail response
    // (realName/scoreState) and the list response (species/scoreEvent).
    final loc = json['publicLocation'] as Map<String, dynamic>? ?? {};
    final scoreState = json['scoreState'] as Map<String, dynamic>?;
    final scoreEvent = json['scoreEvent'] as Map<String, dynamic>?;
    return SubmissionMarker(
      submissionId: json['submissionId'] as String,
      mediaAssetId: json['mediaAssetId'] as String? ?? '',
      latitude: (loc['cellLatitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (loc['cellLongitude'] as num?)?.toDouble() ?? 0.0,
      species:
          (json['realName'] ?? json['species']) as String? ?? 'Unknown',
      points: (scoreState?['visiblePoints'] ?? scoreEvent?['points'])
              as int? ??
          0,
      status: (scoreState?['status'] ?? json['status']) as String? ??
          'pending',
    );
  }

  bool get hasValidLocation => latitude != 0.0 || longitude != 0.0;
}

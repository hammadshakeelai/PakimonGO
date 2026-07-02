class UploadIntentResponse {
  final String mediaAssetId;
  final String uploadUrl;
  final String expiresAt;

  UploadIntentResponse({
    required this.mediaAssetId,
    required this.uploadUrl,
    required this.expiresAt,
  });

  factory UploadIntentResponse.fromJson(Map<String, dynamic> json) {
    return UploadIntentResponse(
      mediaAssetId: json['mediaAssetId'] as String,
      uploadUrl: json['uploadUrl'] as String,
      expiresAt: json['expiresAt'] as String,
    );
  }
}

class CompleteUploadResponse {
  final String status;
  final String mediaAssetId;
  final DerivativeUrls? derivatives;

  CompleteUploadResponse({
    required this.status,
    required this.mediaAssetId,
    this.derivatives,
  });

  factory CompleteUploadResponse.fromJson(Map<String, dynamic> json) {
    return CompleteUploadResponse(
      status: json['status'] as String,
      mediaAssetId: json['mediaAssetId'] as String,
      derivatives: json['derivatives'] != null
          ? DerivativeUrls.fromJson(json['derivatives'] as Map<String, dynamic>)
          : null,
    );
  }
}

class DerivativeUrls {
  final String? thumbnailUrl;
  final String? derivativeUrl;
  final bool exifStripped;

  DerivativeUrls({
    this.thumbnailUrl,
    this.derivativeUrl,
    required this.exifStripped,
  });

  factory DerivativeUrls.fromJson(Map<String, dynamic> json) {
    return DerivativeUrls(
      thumbnailUrl: json['thumbnailUrl'] as String?,
      derivativeUrl: json['derivativeUrl'] as String?,
      exifStripped: json['exifStripped'] as bool,
    );
  }
}

class ScoreState {
  final String status;
  final int? visiblePoints;
  final String? explanationSummary;
  final String? ledger;
  final String? submissionId;

  ScoreState({
    required this.status,
    this.visiblePoints,
    this.explanationSummary,
    this.ledger,
    this.submissionId,
  });

  factory ScoreState.fromJson(Map<String, dynamic> json) {
    return ScoreState(
      status: json['status'] as String,
      visiblePoints: json['visiblePoints'] as int?,
      explanationSummary: json['explanationSummary'] as String?,
      ledger: json['ledger'] as String?,
      submissionId: json['submissionId'] as String?,
    );
  }
}

class SubmissionResponse {
  final String submissionId;
  final String mediaAssetId;
  final ScoreState scoreState;
  final String visibility;
  final Map<String, dynamic> publicLocation;

  SubmissionResponse({
    required this.submissionId,
    required this.mediaAssetId,
    required this.scoreState,
    required this.visibility,
    required this.publicLocation,
  });

  factory SubmissionResponse.fromJson(Map<String, dynamic> json) {
    return SubmissionResponse(
      submissionId: json['submissionId'] as String,
      mediaAssetId: json['mediaAssetId'] as String,
      scoreState: ScoreState.fromJson(json['scoreState'] as Map<String, dynamic>),
      visibility: json['visibility'] as String,
      publicLocation: json['publicLocation'] as Map<String, dynamic>,
    );
  }

  bool get isScored => scoreState.status == 'scored';
  bool get isCapped => scoreState.status == 'capped';
  int get points => scoreState.visiblePoints ?? 0;
}

class UserProfileResponse {
  final String userId;
  final String? email;
  final String? status;
  final String? ageBand;
  final String? homeRegion;
  final String? trustState;

  UserProfileResponse({
    required this.userId,
    this.email,
    this.status,
    this.ageBand,
    this.homeRegion,
    this.trustState,
  });

  factory UserProfileResponse.fromJson(Map<String, dynamic> json) {
    return UserProfileResponse(
      userId: json['userId'] as String,
      email: json['email'] as String?,
      status: json['status'] as String?,
      ageBand: json['ageBand'] as String?,
      homeRegion: json['homeRegion'] as String?,
      trustState: json['trustState'] as String?,
    );
  }
}

import 'submission_marker.dart';

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
  final String? realName;
  final String? animalContext;
  final ScoreState scoreState;
  final String visibility;
  final Map<String, dynamic> publicLocation;

  SubmissionResponse({
    required this.submissionId,
    required this.mediaAssetId,
    this.realName,
    this.animalContext,
    required this.scoreState,
    required this.visibility,
    required this.publicLocation,
  });

  factory SubmissionResponse.fromJson(Map<String, dynamic> json) {
    return SubmissionResponse(
      submissionId: json['submissionId'] as String,
      mediaAssetId: json['mediaAssetId'] as String,
      realName: json['realName'] as String?,
      animalContext: json['animalContext'] as String?,
      scoreState: ScoreState.fromJson(json['scoreState'] as Map<String, dynamic>),
      visibility: json['visibility'] as String,
      publicLocation: json['publicLocation'] as Map<String, dynamic>,
    );
  }

  bool get isScored => scoreState.status == 'scored';
  bool get isCapped => scoreState.status == 'capped';
  int get points => scoreState.visiblePoints ?? 0;

  SubmissionMarker toMarker() {
    return SubmissionMarker(
      submissionId: submissionId,
      mediaAssetId: mediaAssetId,
      species: realName ?? 'Unknown',
      status: scoreState.status,
      points: scoreState.visiblePoints ?? 0,
      latitude: (publicLocation['cellLatitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (publicLocation['cellLongitude'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

class LeaderboardEntry {
  final String userId;
  final String? ageBand;
  final String? homeRegion;
  final int totalScore;
  final int submissionCount;

  LeaderboardEntry({
    required this.userId,
    this.ageBand,
    this.homeRegion,
    required this.totalScore,
    required this.submissionCount,
  });

  factory LeaderboardEntry.fromJson(Map<String, dynamic> json) {
    return LeaderboardEntry(
      userId: json['userId'] as String,
      ageBand: json['ageBand'] as String?,
      homeRegion: json['homeRegion'] as String?,
      totalScore: json['totalScore'] as int? ?? 0,
      submissionCount: json['submissionCount'] as int? ?? 0,
    );
  }
}

class NotificationModel {
  final String id;
  final String notificationType;
  final String title;
  final String? body;
  final String? referenceType;
  final String? referenceId;
  bool isRead;
  final String? createdAt;

  NotificationModel({
    required this.id,
    required this.notificationType,
    required this.title,
    this.body,
    this.referenceType,
    this.referenceId,
    required this.isRead,
    this.createdAt,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'] as String,
      notificationType: json['notificationType'] as String,
      title: json['title'] as String,
      body: json['body'] as String?,
      referenceType: json['referenceType'] as String?,
      referenceId: json['referenceId'] as String?,
      isRead: json['isRead'] as bool,
      createdAt: json['createdAt'] as String?,
    );
  }
}

class CollectionResult {
  final List<CollectionEntry> species;
  final int total;

  CollectionResult({required this.species, required this.total});
}

class CollectionEntry {
  final String species;
  final String? context;
  final int totalPoints;
  final int captureCount;
  final String? lastCaptured;

  CollectionEntry({
    required this.species,
    this.context,
    required this.totalPoints,
    required this.captureCount,
    this.lastCaptured,
  });

  factory CollectionEntry.fromJson(Map<String, dynamic> json) {
    return CollectionEntry(
      species: json['species'] as String,
      context: json['context'] as String?,
      totalPoints: json['totalPoints'] as int? ?? 0,
      captureCount: json['captureCount'] as int? ?? 0,
      lastCaptured: json['lastCaptured'] as String?,
    );
  }
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

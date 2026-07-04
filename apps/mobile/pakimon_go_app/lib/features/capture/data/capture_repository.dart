import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class CaptureRepository {
  final ApiClient _client;

  CaptureRepository({ApiClient? client})
      : _client = client ?? ApiClient();

  Future<UploadIntentResponse> createUploadIntent({
    required String fileName,
    required String contentType,
    required int byteSize,
    required String sha256,
  }) async {
    final response = await _client.post('/media/upload-intent', body: {
      'fileName': fileName,
      'contentType': contentType,
      'byteSize': byteSize,
      'sha256': sha256,
    });
    return UploadIntentResponse.fromJson(response);
  }

  Future<Map<String, dynamic>> uploadFile({
    required String mediaAssetId,
    required List<int> fileBytes,
    required String fileName,
  }) async {
    return _client.putFile(
      '/media/upload/$mediaAssetId',
      fileBytes: fileBytes,
      fileName: fileName,
    );
  }

  Future<CompleteUploadResponse> completeUpload({
    required String mediaAssetId,
    required String sha256,
  }) async {
    final response = await _client.post('/media/complete-upload', body: {
      'mediaAssetId': mediaAssetId,
      'sha256': sha256,
    });
    return CompleteUploadResponse.fromJson(response);
  }

  Future<SubmissionResponse> createSubmission({
    required String mediaAssetId,
    required String animalContext,
    required String realName,
    String? cuteName,
    String? caption,
    List<String>? tags,
    double? latitude,
    double? longitude,
    double? accuracyMeters,
  }) async {
    final body = <String, dynamic>{
      'mediaAssetId': mediaAssetId,
      'animalContext': animalContext,
      'realName': realName,
    };
    if (cuteName != null) body['cuteName'] = cuteName;
    if (caption != null) body['caption'] = caption;
    if (tags != null) body['tags'] = tags;
    if (latitude != null && longitude != null) {
      body['foregroundLocation'] = {
        'latitude': latitude,
        'longitude': longitude,
        'accuracyMeters': accuracyMeters ?? 0,
      };
    }
    final response = await _client.post('/submissions', body: body);
    return SubmissionResponse.fromJson(response);
  }

  Future<SubmissionResponse> getSubmission(String submissionId) async {
    final response = await _client.get('/submissions/$submissionId');
    return SubmissionResponse.fromJson(response);
  }

  Future<UserProfileResponse> getProfile() async {
    final response = await _client.get('/users/me');
    return UserProfileResponse.fromJson(response);
  }

  Future<UserProfileResponse> updateProfile({
    String? ageBand,
    String? homeRegion,
  }) async {
    final body = <String, dynamic>{};
    if (ageBand != null) body['ageBand'] = ageBand;
    if (homeRegion != null) body['homeRegion'] = homeRegion;
    final response = await _client.patch('/users/me', body: body);
    return UserProfileResponse.fromJson(response);
  }

  Future<CollectionResult> getCollection({
    int limit = 20,
    int offset = 0,
    String? context,
    String sortBy = 'totalPoints',
    String sortOrder = 'desc',
  }) async {
    final params = <String, String>{
      'limit': limit.toString(),
      'offset': offset.toString(),
      'sort_by': sortBy,
      'sort_order': sortOrder,
    };
    if (context != null) params['context'] = context;
    final response = await _client.get('/users/me/collection', queryParams: params);
    final speciesList = (response['species'] as List<dynamic>)
        .map((e) => CollectionEntry.fromJson(e as Map<String, dynamic>))
        .toList();
    final pagination = response['pagination'] as Map<String, dynamic>;
    return CollectionResult(
      species: speciesList,
      total: pagination['total'] as int? ?? 0,
    );
  }

  Future<Map<String, dynamic>> getLeaderboard({
    int limit = 20,
    int offset = 0,
  }) async {
    return _client.get('/leaderboard', queryParams: {
      'limit': limit.toString(),
      'offset': offset.toString(),
    }, auth: false);
  }

  Future<Map<String, dynamic>> getSubmissions({
    int limit = 20,
    int offset = 0,
    String? status,
    String sortBy = 'createdAt',
    String sortOrder = 'desc',
  }) async {
    final params = <String, String>{
      'limit': limit.toString(),
      'offset': offset.toString(),
      'sort_by': sortBy,
      'sort_order': sortOrder,
    };
    if (status != null) params['status'] = status;
    return _client.get('/submissions', queryParams: params);
  }

  Future<Map<String, dynamic>> getNotifications({
    int limit = 20,
    int offset = 0,
    bool unreadOnly = false,
  }) async {
    final params = <String, String>{
      'limit': limit.toString(),
      'offset': offset.toString(),
    };
    if (unreadOnly) params['unread_only'] = 'true';
    return _client.get('/notifications', queryParams: params);
  }

  Future<Map<String, dynamic>> markNotificationRead(String notificationId) async {
    return _client.patch('/notifications/$notificationId/read');
  }

  Future<int> getUnreadNotificationCount() async {
    final response = await _client.get('/notifications/unread-count');
    return response['count'] as int;
  }

  Future<List<SubmissionMarker>> getMapMarkers({int limit = 100}) async {
    final response = await _client.get('/submissions', queryParams: {
      'limit': limit.toString(),
      'offset': '0',
      'sort_by': 'createdAt',
      'sort_order': 'desc',
    });
    final items = response['submissions'] as List<dynamic>? ?? [];
    return items
        .map((e) => SubmissionMarker.fromJson(e as Map<String, dynamic>))
        .where((m) => m.hasValidLocation)
        .toList();
  }
}

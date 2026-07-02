import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';

http.Client _mockClient(int status, Map<String, dynamic> body) {
  final bodyStr = jsonEncode(body);
  final stream = http.ByteStream.fromBytes(utf8.encode(bodyStr));
  final response = http.StreamedResponse(stream, status, headers: {
    'content-type': 'application/json',
  });
  return _MockClient(response);
}

class _MockClient extends http.BaseClient {
  final http.StreamedResponse _response;

  _MockClient(this._response);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    return _response;
  }
}

void main() {
  late CaptureRepository repo;

  setUp(() {
    repo = CaptureRepository(
      client: ApiClient(
        client: _mockClient(200, {
          'mediaAssetId': 'media_abc123',
          'uploadUrl': '/media/upload/media_abc123',
          'expiresAt': '2026-07-02T00:00:00Z',
        }),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      ),
    );
  });

  group('CaptureRepository', () {
    test('createUploadIntent parses response', () async {
      final result = await repo.createUploadIntent(
        fileName: 'test.jpg',
        contentType: 'image/jpeg',
        byteSize: 1000,
        sha256: 'a' * 64,
      );
      expect(result.mediaAssetId, 'media_abc123');
      expect(result.uploadUrl, '/media/upload/media_abc123');
    });

    test('completeUpload parses response', () async {
      repo = CaptureRepository(
        client: ApiClient(
          client: _mockClient(200, {
            'status': 'ok',
            'mediaAssetId': 'media_abc123',
            'derivatives': {
              'thumbnailUrl': '/thumbs/media_abc123.webp',
              'derivativeUrl': '/public/media_abc123.webp',
              'exifStripped': true,
            },
          }),
          baseUrl: 'http://test/api',
          tokenProvider: () => 'test',
        ),
      );
      final result = await repo.completeUpload(
        mediaAssetId: 'media_abc123',
        sha256: 'a' * 64,
      );
      expect(result.status, 'ok');
      expect(result.derivatives?.thumbnailUrl, '/thumbs/media_abc123.webp');
      expect(result.derivatives?.exifStripped, true);
    });

    test('createSubmission parses response', () async {
      repo = CaptureRepository(
        client: ApiClient(
          client: _mockClient(200, {
            'submissionId': 'sub_test123',
            'mediaAssetId': 'media_abc123',
            'scoreState': {
              'status': 'ai_evaluated',
              'visiblePoints': null,
              'explanationSummary': 'pending',
              'ledger': 'wild',
            },
            'visibility': 'private',
            'publicLocation': {
              'cellId': 'cell_abcd1234',
              'precisionLabel': 'coarse',
            },
          }),
          baseUrl: 'http://test/api',
          tokenProvider: () => 'test',
        ),
      );
      final result = await repo.createSubmission(
        mediaAssetId: 'media_abc123',
        animalContext: 'wild',
        realName: 'Passer domesticus',
      );
      expect(result.submissionId, 'sub_test123');
      expect(result.scoreState.status, 'ai_evaluated');
      expect(result.isScored, false);
      expect(result.points, 0);
    });

    test('getProfile parses response', () async {
      repo = CaptureRepository(
        client: ApiClient(
          client: _mockClient(200, {
            'userId': 'test_user',
            'email': 'test@example.com',
          }),
          baseUrl: 'http://test/api',
          tokenProvider: () => 'test',
        ),
      );
      final result = await repo.getProfile();
      expect(result.userId, 'test_user');
      expect(result.email, 'test@example.com');
    });

    test('throws on error response', () async {
      repo = CaptureRepository(
        client: ApiClient(
          client: _mockClient(400, {'detail': 'Missing mediaAssetId'}),
          baseUrl: 'http://test/api',
          tokenProvider: () => 'test',
        ),
      );
      expect(
        () => repo.createUploadIntent(
          fileName: 'test.jpg',
          contentType: 'image/jpeg',
          byteSize: 1000,
          sha256: 'a' * 64,
        ),
        throwsA(isA<ApiException>()),
      );
    });
  });
}

import 'dart:convert';

import 'package:http/http.dart' as http;

/// Shared mock client + fixture for the collection viewmodel/screen tests.
class MockCollectionClient extends http.BaseClient {
  final Map<String, http.Response> responses;

  MockCollectionClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url}';
    final resp = responses[key];
    if (resp != null) {
      return http.StreamedResponse(
        http.ByteStream.fromBytes(resp.bodyBytes),
        resp.statusCode,
        headers: resp.headers,
      );
    }
    return http.StreamedResponse(
      http.ByteStream.fromBytes(utf8.encode('{"detail": "not found"}')),
      404,
    );
  }
}

Map<String, dynamic> collectionJson() => {
      'userId': 'user-123',
      'species': [
        {
          'species': 'Markhor',
          'context': 'wild',
          'totalPoints': 75,
          'captureCount': 3,
          'lastCaptured': '2026-07-03T10:00:00',
          'submissionId': 'sub_markhor_latest',
          'mediaAssetId': 'media_markhor_latest',
          'publicLocation': {
            'cellId': 'cell_33.68_73.05',
            'cellLatitude': 33.68,
            'cellLongitude': 73.05,
          },
        },
        {
          'species': 'Peacock',
          'context': 'zoo',
          'totalPoints': 5,
          'captureCount': 5,
          'lastCaptured': '2026-07-02T10:00:00',
          'submissionId': null,
          'mediaAssetId': null,
          'publicLocation': null,
        },
      ],
      'pagination': {'limit': 20, 'offset': 0, 'total': 2},
    };

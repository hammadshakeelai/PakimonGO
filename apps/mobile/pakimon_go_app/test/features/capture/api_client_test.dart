import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';

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
  group('ApiClient', () {
    test('GET returns parsed JSON', () async {
      final client = ApiClient(
        client: _mockClient(200, {'status': 'ok'}),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      );
      final result = await client.get('/health');
      expect(result, {'status': 'ok'});
    });

    test('POST sends body and returns parsed JSON', () async {
      final client = ApiClient(
        client: _mockClient(200, {'id': 'sub_123'}),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      );
      final result = await client.post('/submissions', body: {'key': 'val'});
      expect(result, {'id': 'sub_123'});
    });

    test('throws ApiException on error status', () async {
      final client = ApiClient(
        client: _mockClient(404, {'detail': 'Not found'}),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      );
      expect(
        () => client.get('/missing'),
        throwsA(isA<ApiException>().having(
          (e) => e.statusCode,
          'statusCode',
          404,
        )),
      );
    });

    test('throws ApiException with detail message', () async {
      final client = ApiClient(
        client: _mockClient(400, {'detail': 'Missing field'}),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      );
      expect(
        () => client.post('/test'),
        throwsA(isA<ApiException>().having(
          (e) => e.message,
          'message',
          'Missing field',
        )),
      );
    });

    test('GET without auth works', () async {
      final client = ApiClient(
        client: _mockClient(200, {'entries': []}),
        baseUrl: 'http://test/api',
        tokenProvider: () => 'test',
      );
      final result = await client.get('/public', auth: false);
      expect(result, {'entries': []});
    });
  });
}

import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_config.dart';

class ApiClient {
  final http.Client _client;
  final String _baseUrl;
  final String Function() _tokenProvider;

  ApiClient({
    http.Client? client,
    String? baseUrl,
    String Function()? tokenProvider,
  })  : _client = client ?? http.Client(),
        _baseUrl = baseUrl ?? ApiConfig.apiBase,
        _tokenProvider = tokenProvider ?? (() => ApiConfig.authToken);

  Map<String, String> _headers({bool auth = true}) {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (auth) {
      headers['Authorization'] = 'Bearer ${_tokenProvider()}';
    }
    return headers;
  }

  Future<Map<String, dynamic>> get(
    String path, {
    Map<String, String>? queryParams,
    bool auth = true,
  }) async {
    final uri = Uri.parse('$_baseUrl$path')
        .replace(queryParameters: queryParams);
    final response = await _client.get(uri, headers: _headers(auth: auth));
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> post(
    String path, {
    Map<String, dynamic>? body,
    bool auth = true,
  }) async {
    final uri = Uri.parse('$_baseUrl$path');
    final response = await _client.post(
      uri,
      headers: _headers(auth: auth),
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> patch(
    String path, {
    Map<String, dynamic>? body,
    bool auth = true,
  }) async {
    final uri = Uri.parse('$_baseUrl$path');
    final response = await _client.patch(
      uri,
      headers: _headers(auth: auth),
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> putFile(
    String path, {
    required List<int> fileBytes,
    required String fileName,
    String contentType = 'image/jpeg',
    bool auth = true,
  }) async {
    final uri = Uri.parse('$_baseUrl$path');
    final request = http.MultipartRequest('PUT', uri);
    if (auth) {
      request.headers['Authorization'] = 'Bearer ${_tokenProvider()}';
    }
    request.files.add(http.MultipartFile.fromBytes(
      'file',
      fileBytes,
      filename: fileName,
    ));
    final streamed = await _client.send(request);
    final response = await http.Response.fromStream(streamed);
    return _handleResponse(response);
  }

  Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return {'status': 'ok'};
      return jsonDecode(response.body) as Map<String, dynamic>;
    }
    throw ApiException(
      statusCode: response.statusCode,
      message: response.body.isNotEmpty
          ? (jsonDecode(response.body)['detail'] ?? response.body) as String
          : 'Request failed',
    );
  }

  void close() {
    _client.close();
  }
}

class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException({required this.statusCode, required this.message});

  @override
  String toString() => 'ApiException($statusCode): $message';
}

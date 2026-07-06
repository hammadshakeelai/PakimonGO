import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'api_config.dart';

class ApiClient {
  final http.Client _client;
  final String _baseUrl;
  final FutureOr<String> Function() _tokenProvider;
  final Duration _timeout;

  ApiClient({
    http.Client? client,
    String? baseUrl,
    FutureOr<String> Function()? tokenProvider,
    Duration timeout = const Duration(seconds: 15),
  })  : _client = client ?? http.Client(),
        _baseUrl = baseUrl ?? ApiConfig.apiBase,
        _tokenProvider = tokenProvider ?? (() => ApiConfig.authToken),
        _timeout = timeout;

  /// Async because the token provider may need to refresh an expired
  /// Firebase ID token before the request goes out.
  Future<Map<String, String>> _headers({bool auth = true}) async {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (auth) {
      headers['Authorization'] = 'Bearer ${await _tokenProvider()}';
    }
    return headers;
  }

  Future<Map<String, dynamic>> get(
    String path, {
    Map<String, String>? queryParams,
    bool auth = true,
  }) {
    final uri =
        Uri.parse('$_baseUrl$path').replace(queryParameters: queryParams);
    return _send(() async => _client.get(uri, headers: await _headers(auth: auth)));
  }

  Future<Map<String, dynamic>> post(
    String path, {
    Map<String, dynamic>? body,
    bool auth = true,
  }) {
    final uri = Uri.parse('$_baseUrl$path');
    return _send(() async => _client.post(
          uri,
          headers: await _headers(auth: auth),
          body: body != null ? jsonEncode(body) : null,
        ));
  }

  Future<Map<String, dynamic>> patch(
    String path, {
    Map<String, dynamic>? body,
    bool auth = true,
  }) {
    final uri = Uri.parse('$_baseUrl$path');
    return _send(() async => _client.patch(
          uri,
          headers: await _headers(auth: auth),
          body: body != null ? jsonEncode(body) : null,
        ));
  }

  Future<Map<String, dynamic>> delete(
    String path, {
    bool auth = true,
  }) {
    final uri = Uri.parse('$_baseUrl$path');
    return _send(() async => _client.delete(uri, headers: await _headers(auth: auth)));
  }

  Future<Map<String, dynamic>> putFile(
    String path, {
    required List<int> fileBytes,
    required String fileName,
    String contentType = 'image/jpeg',
    bool auth = true,
  }) {
    final uri = Uri.parse('$_baseUrl$path');
    return _send(() async {
      final request = http.MultipartRequest('PUT', uri);
      if (auth) {
        request.headers['Authorization'] = 'Bearer ${await _tokenProvider()}';
      }
      request.files.add(http.MultipartFile.fromBytes(
        'file',
        fileBytes,
        filename: fileName,
      ));
      final streamed = await _client.send(request);
      return http.Response.fromStream(streamed);
    });
  }

  /// Runs [request] with a timeout and normalizes transport failures
  /// (timeout / offline / server unreachable) into an [ApiException] so callers
  /// only ever have to catch one error type.
  Future<Map<String, dynamic>> _send(
    Future<http.Response> Function() request,
  ) async {
    try {
      final response = await request().timeout(_timeout);
      return _handleResponse(response);
    } on ApiException {
      rethrow;
    } on TimeoutException {
      throw ApiException(
        statusCode: 0,
        message: 'The request timed out. Check your connection and try again.',
        isNetworkError: true,
      );
    } on SocketException {
      throw ApiException(
        statusCode: 0,
        message: 'No internet connection. Please check your network.',
        isNetworkError: true,
      );
    } on http.ClientException {
      throw ApiException(
        statusCode: 0,
        message: 'Could not reach the server. Please try again.',
        isNetworkError: true,
      );
    }
  }

  Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return {'status': 'ok'};
      return jsonDecode(response.body) as Map<String, dynamic>;
    }
    throw ApiException(
      statusCode: response.statusCode,
      message: _extractErrorMessage(response),
    );
  }

  /// Pulls a human-readable message out of either the backend's structured
  /// error (`{"error": {"message": ...}}`) or FastAPI's `{"detail": ...}` shape
  /// (which is a list for 422 validation errors).
  String _extractErrorMessage(http.Response response) {
    final fallback = 'Request failed (${response.statusCode}).';
    if (response.body.isEmpty) return fallback;
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map<String, dynamic>) {
        final error = decoded['error'];
        if (error is Map && error['message'] is String) {
          return error['message'] as String;
        }
        final detail = decoded['detail'];
        if (detail is String) return detail;
        if (detail is List && detail.isNotEmpty) {
          final first = detail.first;
          if (first is Map && first['msg'] is String) {
            return first['msg'] as String;
          }
          return detail.map((e) => e.toString()).join('; ');
        }
      }
    } catch (_) {
      // Body was not JSON — fall through to the generic message.
    }
    return fallback;
  }

  void close() {
    _client.close();
  }
}

class ApiException implements Exception {
  final int statusCode;
  final String message;

  /// True when the failure was a transport problem (timeout / offline /
  /// server unreachable) rather than an HTTP error response from the server.
  final bool isNetworkError;

  ApiException({
    required this.statusCode,
    required this.message,
    this.isNetworkError = false,
  });

  @override
  String toString() => 'ApiException($statusCode): $message';
}

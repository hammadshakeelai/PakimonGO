class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  static const String authToken = String.fromEnvironment(
    'AUTH_TOKEN',
    defaultValue: 'test_token_valid',
  );

  static const String uploadBase = String.fromEnvironment(
    'UPLOAD_BASE_URL',
    defaultValue: '$baseUrl/v1/media',
  );

  static const String submissionsBase = String.fromEnvironment(
    'SUBMISSIONS_BASE_URL',
    defaultValue: '$baseUrl/v1/submissions',
  );

  static const String apiBase = String.fromEnvironment(
    'API_BASE',
    defaultValue: '$baseUrl/v1',
  );
}

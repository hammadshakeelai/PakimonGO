class AppConfig {
  static const String mapboxAccessToken = String.fromEnvironment(
    'MAPBOX_ACCESS_TOKEN',
    defaultValue: '',
  );

  static bool get hasMapboxToken => mapboxAccessToken.isNotEmpty;
}

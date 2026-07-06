import 'package:geolocator/geolocator.dart';

/// A device GPS fix captured at submission time.
class DeviceLocation {
  final double latitude;
  final double longitude;
  final double? accuracyMeters;

  const DeviceLocation({
    required this.latitude,
    required this.longitude,
    this.accuracyMeters,
  });
}

/// Abstraction over the platform location plugin so screens are testable.
abstract class LocationService {
  /// Returns the current device location, or null when the user denies
  /// permission, location services are off, or the fix times out.
  Future<DeviceLocation?> getCurrentLocation();
}

class GeolocatorLocationService implements LocationService {
  @override
  Future<DeviceLocation?> getCurrentLocation() async {
    try {
      if (!await Geolocator.isLocationServiceEnabled()) return null;

      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        return null;
      }

      final position = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          timeLimit: Duration(seconds: 10),
        ),
      );
      return DeviceLocation(
        latitude: position.latitude,
        longitude: position.longitude,
        accuracyMeters: position.accuracy,
      );
    } catch (_) {
      // Fresh fix failed (timeout / plugin unavailable) — try the cache.
      try {
        final last = await Geolocator.getLastKnownPosition();
        if (last == null) return null;
        return DeviceLocation(
          latitude: last.latitude,
          longitude: last.longitude,
          accuracyMeters: last.accuracy,
        );
      } catch (_) {
        return null;
      }
    }
  }
}

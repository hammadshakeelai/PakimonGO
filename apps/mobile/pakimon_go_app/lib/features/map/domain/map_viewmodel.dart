import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/map/domain/cluster_service.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class MapViewModel extends ChangeNotifier {
  final CaptureRepository _repository;
  List<SubmissionMarker> _markers = [];
  List<ClusterMarker> _clusters = [];
  bool _isLoading = false;
  String? _error;
  bool _isOffline = false;

  MapViewModel({required CaptureRepository repository})
      : _repository = repository;

  bool _disposed = false;

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }

  void _notify() {
    // An in-flight fetch can complete after the owning screen is gone;
    // notifying a disposed ChangeNotifier crashes the app.
    if (!_disposed) notifyListeners();
  }

  List<SubmissionMarker> get markers => _markers;
  List<ClusterMarker> get clusters => _clusters;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isOffline => _isOffline;
  int get markerCount => _markers.length;
  int get clusterCount => _clusters.length;
  bool get hasMarkers => _markers.isNotEmpty;

  Future<void> fetchMarkers() async {
    _isLoading = true;
    _error = null;
    _isOffline = false;
    _notify();

    try {
      _markers = await _repository.getMapMarkers();
      _clusters = _buildClusters();
    } catch (e) {
      _isOffline = e is ApiException && e.isNetworkError;
      _error = e is ApiException
          ? e.message
          : 'Something went wrong. Please try again.';
      _markers = [];
      _clusters = [];
    }

    _isLoading = false;
    _notify();
  }

  List<ClusterMarker> _buildClusters() {
    if (_markers.length <= 3) return [];
    return ClusterService.cluster(_markers);
  }
}

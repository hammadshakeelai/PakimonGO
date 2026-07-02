import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/map/domain/cluster_service.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class MapViewModel extends ChangeNotifier {
  final CaptureRepository _repository;
  List<SubmissionMarker> _markers = [];
  List<ClusterMarker> _clusters = [];
  bool _isLoading = false;
  String? _error;

  MapViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<SubmissionMarker> get markers => _markers;
  List<ClusterMarker> get clusters => _clusters;
  bool get isLoading => _isLoading;
  String? get error => _error;
  int get markerCount => _markers.length;
  int get clusterCount => _clusters.length;
  bool get hasMarkers => _markers.isNotEmpty;

  Future<void> fetchMarkers() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _markers = await _repository.getMapMarkers();
      _clusters = _buildClusters();
    } catch (e) {
      _error = e.toString();
      _markers = [];
      _clusters = [];
    }

    _isLoading = false;
    notifyListeners();
  }

  List<ClusterMarker> _buildClusters() {
    if (_markers.length <= 3) return [];
    return ClusterService.cluster(_markers);
  }
}

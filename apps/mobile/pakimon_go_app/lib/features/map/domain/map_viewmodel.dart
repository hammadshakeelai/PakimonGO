import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class MapViewModel extends ChangeNotifier {
  final CaptureRepository _repository;
  List<SubmissionMarker> _markers = [];
  bool _isLoading = false;
  String? _error;

  MapViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<SubmissionMarker> get markers => _markers;
  bool get isLoading => _isLoading;
  String? get error => _error;
  int get markerCount => _markers.length;
  bool get hasMarkers => _markers.isNotEmpty;

  Future<void> fetchMarkers() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _markers = await _repository.getMapMarkers();
    } catch (e) {
      _error = e.toString();
      _markers = [];
    }

    _isLoading = false;
    notifyListeners();
  }
}

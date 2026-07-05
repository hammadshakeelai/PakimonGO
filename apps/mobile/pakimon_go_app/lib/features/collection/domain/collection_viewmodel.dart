import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class CollectionViewModel extends ChangeNotifier {
  final CaptureRepository _repository;

  CollectionViewModel({required CaptureRepository repository})
      : _repository = repository;

  CollectionLoadState _state = CollectionLoadState.loading;
  CollectionLoadState get state => _state;

  List<CollectionEntry> _entries = [];
  List<CollectionEntry> get entries => _entries;

  int _total = 0;
  int get total => _total;

  String? _error;
  String? get error => _error;

  bool _isOffline = false;
  bool get isOffline => _isOffline;

  String _sortBy = 'totalPoints';
  String get sortBy => _sortBy;

  String _sortOrder = 'desc';
  String get sortOrder => _sortOrder;

  String? _contextFilter;
  String? get contextFilter => _contextFilter;

  Future<void> fetchCollection() async {
    _state = CollectionLoadState.loading;
    _error = null;
    _isOffline = false;
    notifyListeners();

    try {
      final result = await _repository.getCollection(
        context: _contextFilter,
        sortBy: _sortBy,
        sortOrder: _sortOrder,
      );
      _entries = result.species;
      _total = result.total;
      _state = _entries.isEmpty
          ? CollectionLoadState.empty
          : CollectionLoadState.loaded;
    } catch (e) {
      _isOffline = e is ApiException && e.isNetworkError;
      _error = e is ApiException
          ? e.message
          : 'Something went wrong. Please try again.';
      _state = CollectionLoadState.error;
    }
    notifyListeners();
  }

  void setSortBy(String value) {
    _sortBy = value;
    fetchCollection();
  }

  void setSortOrder(String value) {
    _sortOrder = value;
    fetchCollection();
  }

  void setContextFilter(String? value) {
    _contextFilter = value;
    fetchCollection();
  }

  void refresh() => fetchCollection();
}

enum CollectionLoadState { loading, loaded, empty, error }

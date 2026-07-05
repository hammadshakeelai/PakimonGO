import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class LeaderboardViewModel extends ChangeNotifier {
  final CaptureRepository _repository;

  List<LeaderboardEntry> _entries = [];
  int _total = 0;
  final int _limit;
  bool _isLoading = false;
  String? _error;
  bool _isOffline = false;

  LeaderboardViewModel({required CaptureRepository repository})
      : _repository = repository,
        _limit = 50;

  CaptureRepository get repository => _repository;

  List<LeaderboardEntry> get entries => _entries;
  int get total => _total;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isOffline => _isOffline;

  Future<void> fetchLeaderboard() async {
    _isLoading = true;
    _error = null;
    _isOffline = false;
    notifyListeners();

    try {
      final response = await _repository.getLeaderboard(limit: _limit);
      final raw = response['entries'] as List<dynamic>? ?? [];
      _entries = raw
          .map((e) => LeaderboardEntry.fromJson(e as Map<String, dynamic>))
          .toList();
      _total = _entries.length;
    } catch (e) {
      _isOffline = e is ApiException && e.isNetworkError;
      _error = e is ApiException
          ? e.message
          : 'Something went wrong. Please try again.';
    }

    _isLoading = false;
    notifyListeners();
  }
}

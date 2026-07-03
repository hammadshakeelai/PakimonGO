import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class LeaderboardViewModel extends ChangeNotifier {
  final CaptureRepository _repository;

  List<LeaderboardEntry> _entries = [];
  int _total = 0;
  int _limit = 50;
  bool _isLoading = false;
  String? _error;

  LeaderboardViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<LeaderboardEntry> get entries => _entries;
  int get total => _total;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchLeaderboard() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _repository.getLeaderboard(limit: _limit);
      final raw = response['entries'] as List<dynamic>? ?? [];
      _entries = raw
          .map((e) => LeaderboardEntry.fromJson(e as Map<String, dynamic>))
          .toList();
      _total = _entries.length;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }
}

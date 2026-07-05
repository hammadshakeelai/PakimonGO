import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';

class BlockedUsersViewModel extends ChangeNotifier {
  final CaptureRepository _repository;
  List<String> _blockedUserIds = [];
  bool _isLoading = false;
  String? _error;
  bool _isOffline = false;
  bool _disposed = false;

  BlockedUsersViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<String> get blockedUserIds => _blockedUserIds;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isOffline => _isOffline;
  bool get isEmpty => _blockedUserIds.isEmpty && !_isLoading;

  CaptureRepository get repository => _repository;

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }

  void _notify() {
    if (!_disposed) notifyListeners();
  }

  Future<void> fetchBlockedUsers() async {
    _isLoading = true;
    _error = null;
    _isOffline = false;
    _notify();

    try {
      final json = await _repository.getBlockedUsers();
      final items = json['items'] as List<dynamic>;
      _blockedUserIds = items
          .map((e) => (e as Map<String, dynamic>)['blockedUserId'] as String)
          .toList();
    } catch (e) {
      _isOffline = e is ApiException && e.isNetworkError;
      _error = e is ApiException
          ? e.message
          : 'Something went wrong. Please try again.';
    }

    _isLoading = false;
    _notify();
  }

  Future<bool> unblock(String userId) async {
    try {
      await _repository.unblockUser(userId);
      _blockedUserIds.remove(userId);
      _notify();
      return true;
    } catch (_) {
      return false;
    }
  }
}

import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class NotificationViewModel extends ChangeNotifier {
  final CaptureRepository _repository;

  List<NotificationModel> _notifications = [];
  int _total = 0;
  int _unreadCount = 0;
  bool _isLoading = false;
  String? _error;

  NotificationViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<NotificationModel> get notifications => _notifications;
  int get total => _total;
  int get unreadCount => _unreadCount;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchNotifications({bool unreadOnly = false}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _repository.getNotifications(
        unreadOnly: unreadOnly,
      );
      final items = (response['items'] as List<dynamic>?)
              ?.map((e) => NotificationModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];
      _notifications = items;
      _total = response['total'] as int? ?? 0;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<void> fetchUnreadCount() async {
    try {
      _unreadCount = await _repository.getUnreadNotificationCount();
      notifyListeners();
    } catch (_) {}
  }

  Future<void> markAsRead(NotificationModel notification) async {
    if (notification.isRead) return;
    try {
      await _repository.markNotificationRead(notification.id);
      notification.isRead = true;
      if (_unreadCount > 0) _unreadCount--;
      notifyListeners();
    } catch (_) {}
  }

  Future<SubmissionResponse?> getSubmissionById(String id) async {
    try {
      return await _repository.getSubmission(id);
    } catch (_) {
      return null;
    }
  }
}

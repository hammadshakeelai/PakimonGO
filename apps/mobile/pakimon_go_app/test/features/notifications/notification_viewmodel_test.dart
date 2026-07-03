import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/notifications/domain/notification_viewmodel.dart';

class _MockClient extends http.BaseClient {
  final Map<String, http.StreamedResponse> responses;

  _MockClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url.path}';
    final resp = responses[key];
    if (resp != null) return resp;
    return http.StreamedResponse(
      Stream.value(utf8.encode('{"error":"not found"}')),
      404,
    );
  }
}

ApiClient _makeClient(Map<String, http.StreamedResponse> responses) {
  return ApiClient(baseUrl: 'http://test', client: _MockClient(responses));
}

http.StreamedResponse _jsonResponse(int status, Map<String, dynamic> body) {
  return http.StreamedResponse(
    Stream.value(utf8.encode(jsonEncode(body))),
    status,
    headers: {'content-type': 'application/json'},
  );
}

void main() {
  group('NotificationViewModel', () {
    test('starts empty', () {
      final vm = NotificationViewModel(
        repository: CaptureRepository(client: ApiClient()),
      );
      expect(vm.notifications, isEmpty);
      expect(vm.isLoading, false);
      expect(vm.error, isNull);
      expect(vm.unreadCount, 0);
    });

    test('fetchNotifications populates list', () async {
      final client = _makeClient({
        'GET /notifications': _jsonResponse(200, {
          'items': [
            {
              'id': 'n1',
              'notificationType': 'submission_scored',
              'title': 'Scored: 25 pts',
              'body': 'Your submission received 25 points.',
              'isRead': false,
              'createdAt': '2026-07-03T00:00:00Z',
            }
          ],
          'total': 1,
        }),
      });
      final vm = NotificationViewModel(
        repository: CaptureRepository(client: client),
      );

      await vm.fetchNotifications();

      expect(vm.isLoading, false);
      expect(vm.error, isNull);
      expect(vm.notifications.length, 1);
      expect(vm.notifications[0].title, 'Scored: 25 pts');
      expect(vm.notifications[0].isRead, false);
    });

    test('fetchNotifications handles error', () async {
      final client = _makeClient({
        'GET /notifications': _jsonResponse(500, {'error': 'server error'}),
      });
      final vm = NotificationViewModel(
        repository: CaptureRepository(client: client),
      );

      await vm.fetchNotifications();

      expect(vm.isLoading, false);
      expect(vm.error, isNotNull);
      expect(vm.notifications, isEmpty);
    });

    test('markAsRead updates state', () async {
      final client = _makeClient({
        'GET /notifications': _jsonResponse(200, {
          'items': [
            {
              'id': 'n1',
              'notificationType': 'test',
              'title': 'Test',
              'isRead': false,
            }
          ],
          'total': 1,
        }),
        'PATCH /notifications/n1/read': _jsonResponse(200, {
          'status': 'ok',
          'notification': {'id': 'n1', 'isRead': true},
        }),
      });
      final vm = NotificationViewModel(
        repository: CaptureRepository(client: client),
      );
      await vm.fetchNotifications();
      expect(vm.notifications[0].isRead, false);

      await vm.markAsRead(vm.notifications[0]);

      expect(vm.notifications[0].isRead, true);
    });

    test('fetchUnreadCount updates count', () async {
      final client = _makeClient({
        'GET /notifications/unread-count': _jsonResponse(200, {'count': 5}),
      });
      final vm = NotificationViewModel(
        repository: CaptureRepository(client: client),
      );

      await vm.fetchUnreadCount();

      expect(vm.unreadCount, 5);
    });
  });
}

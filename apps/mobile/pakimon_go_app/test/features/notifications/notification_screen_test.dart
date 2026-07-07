import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/notifications/domain/notification_viewmodel.dart';
import 'package:pakimon_go_app/features/notifications/presentation/notification_screen.dart';

class _EmptyClient extends http.BaseClient {
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    return http.StreamedResponse(
      Stream.value(utf8.encode('{"items":[],"total":0}')),
      200,
      headers: {'content-type': 'application/json'},
    );
  }
}

class _MockClient extends http.BaseClient {
  final Map<String, http.Response> responses;

  _MockClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url}';
    final resp = responses[key];
    if (resp != null) {
      return http.StreamedResponse(
        http.ByteStream.fromBytes(resp.bodyBytes),
        resp.statusCode,
        headers: resp.headers,
      );
    }
    return http.StreamedResponse(
      http.ByteStream.fromBytes(utf8.encode('{"detail": "not found"}')),
      404,
    );
  }
}

class _ErrorClient extends http.BaseClient {
  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    return http.StreamedResponse(
      Stream.value(utf8.encode('{"error":"fail"}')),
      500,
    );
  }
}

Widget _buildTestApp(NotificationViewModel vm) {
  return MaterialApp(
    home: NotificationScreen(viewModel: vm),
  );
}

void main() {
  testWidgets('shows loading indicator initially', (WidgetTester tester) async {
    final vm = NotificationViewModel(
      repository: CaptureRepository(client: ApiClient(client: _EmptyClient())),
    );
    vm.fetchNotifications();

    await tester.pumpWidget(_buildTestApp(vm));

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('shows empty state when no notifications',
      (WidgetTester tester) async {
    final vm = NotificationViewModel(
      repository: CaptureRepository(client: ApiClient(client: _EmptyClient())),
    );
    await vm.fetchNotifications();
    await tester.pumpWidget(_buildTestApp(vm));
    await tester.pumpAndSettle();

    expect(find.text('No notifications yet'), findsOneWidget);
  });

  testWidgets('shows error state with retry', (WidgetTester tester) async {
    final vm = NotificationViewModel(
      repository: CaptureRepository(client: ApiClient(client: _ErrorClient())),
    );
    await vm.fetchNotifications();
    await tester.pumpWidget(_buildTestApp(vm));
    await tester.pumpAndSettle();

    expect(find.text('Failed to load notifications'), findsOneWidget);
    expect(find.text('Retry'), findsOneWidget);
  });

  testWidgets('tapping submission notification navigates to detail',
      (WidgetTester tester) async {
    final notificationId = 'notif-1';
    final submissionId = 'sub-456';
    final notifJson = {
      'items': [
        {
          'id': notificationId,
          'notificationType': 'score',
          'title': 'Submission Scored!',
          'body': 'Your Markhor earned 75 points',
          'referenceType': 'submission',
          'referenceId': submissionId,
          'isRead': false,
          'createdAt': '2026-07-03T10:00:00',
        }
      ],
      'total': 1,
    };
    final subJson = {
      'submissionId': submissionId,
      'userId': 'user-123',
      'mediaAssetId': 'media-789',
      'realName': 'Markhor',
      'animalContext': 'wild',
      'species': 'Markhor',
      'status': 'scored',
      'visibility': 'public',
      'scoreState': {
        'status': 'scored',
        'visiblePoints': 75,
        'explanationSummary': 'Wild animal detected',
      },
      'publicLocation': {'cellLatitude': 33.7, 'cellLongitude': 73.1},
      'createdAt': '2026-07-03T10:00:00',
    };

    final responses = <String, http.Response>{
      'GET http://test.com/notifications?limit=20&offset=0':
          http.Response(jsonEncode(notifJson), 200, headers: {'content-type': 'application/json'}),
      'GET http://test.com/notifications/unread-count':
          http.Response(jsonEncode({'count': 1}), 200, headers: {'content-type': 'application/json'}),
      'PATCH http://test.com/notifications/$notificationId/read':
          http.Response('{}', 200, headers: {'content-type': 'application/json'}),
      'GET http://test.com/submissions/$submissionId':
          http.Response(jsonEncode(subJson), 200, headers: {'content-type': 'application/json'}),
    };

    final client = _MockClient(responses);

    final vm = NotificationViewModel(
      repository: CaptureRepository(
        client: ApiClient(client: client, baseUrl: 'http://test.com'),
      ),
    );
    await vm.fetchNotifications();
    await tester.pumpWidget(_buildTestApp(vm));
    await tester.pumpAndSettle();

    expect(find.text('Submission Scored!'), findsOneWidget);

    await tester.tap(find.text('Submission Scored!'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));

    expect(find.text('Markhor'), findsAtLeast(1));
  });
}

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
}

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/moderation/domain/blocked_users_viewmodel.dart';
import 'package:pakimon_go_app/features/moderation/presentation/blocked_users_screen.dart';
import 'package:pakimon_go_app/features/moderation/presentation/report_dialog.dart';

class _MockClient extends http.BaseClient {
  final Map<String, http.StreamedResponse Function()> responses;
  final List<String> calls = [];

  _MockClient(this.responses);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final key = '${request.method} ${request.url.path}';
    calls.add(key);
    final make = responses[key];
    if (make != null) return make();
    return http.StreamedResponse(
      Stream.value(utf8.encode('{"detail":"not found"}')),
      404,
    );
  }
}

http.StreamedResponse _json(int status, Map<String, dynamic> body) {
  return http.StreamedResponse(
    Stream.value(utf8.encode(jsonEncode(body))),
    status,
    headers: {'content-type': 'application/json'},
  );
}

CaptureRepository _repo(_MockClient client) => CaptureRepository(
      client: ApiClient(baseUrl: 'http://test', client: client),
    );

void main() {
  group('CaptureRepository moderation calls', () {
    test('submitReport posts to /reports', () async {
      final client = _MockClient({
        'POST /reports': () => _json(201, {
              'reportId': 'r1',
              'targetType': 'submission',
              'targetId': 's1',
              'reason': 'spam',
              'status': 'open',
            }),
      });
      final result = await _repo(client).submitReport(
        targetType: 'submission',
        targetId: 's1',
        reason: 'spam',
      );
      expect(result['reportId'], 'r1');
      expect(client.calls, contains('POST /reports'));
    });

    test('blockUser / unblockUser hit /blocks/{id}', () async {
      final client = _MockClient({
        'POST /blocks/u2': () => _json(201, {'blockedUserId': 'u2'}),
        'DELETE /blocks/u2': () =>
            _json(200, {'status': 'ok', 'blockedUserId': 'u2'}),
      });
      final repo = _repo(client);
      await repo.blockUser('u2');
      await repo.unblockUser('u2');
      expect(client.calls,
          containsAll(['POST /blocks/u2', 'DELETE /blocks/u2']));
    });
  });

  group('BlockedUsersViewModel', () {
    test('fetches blocked users', () async {
      final client = _MockClient({
        'GET /blocks': () => _json(200, {
              'items': [
                {'blockedUserId': 'u2', 'createdAt': null},
                {'blockedUserId': 'u3', 'createdAt': null},
              ],
              'total': 2,
            }),
      });
      final vm = BlockedUsersViewModel(repository: _repo(client));
      await vm.fetchBlockedUsers();
      expect(vm.blockedUserIds, ['u2', 'u3']);
      expect(vm.error, isNull);
    });

    test('unblock removes the user from the list', () async {
      final client = _MockClient({
        'GET /blocks': () => _json(200, {
              'items': [
                {'blockedUserId': 'u2', 'createdAt': null},
              ],
              'total': 1,
            }),
        'DELETE /blocks/u2': () =>
            _json(200, {'status': 'ok', 'blockedUserId': 'u2'}),
      });
      final vm = BlockedUsersViewModel(repository: _repo(client));
      await vm.fetchBlockedUsers();
      final ok = await vm.unblock('u2');
      expect(ok, isTrue);
      expect(vm.blockedUserIds, isEmpty);
    });

    test('reports errors', () async {
      final vm = BlockedUsersViewModel(repository: _repo(_MockClient({})));
      await vm.fetchBlockedUsers();
      expect(vm.error, isNotNull);
    });
  });

  group('BlockedUsersScreen', () {
    testWidgets('shows empty state', (tester) async {
      final client = _MockClient({
        'GET /blocks': () => _json(200, {'items': [], 'total': 0}),
      });
      await tester.pumpWidget(MaterialApp(
        home: BlockedUsersScreen(
          viewModel: BlockedUsersViewModel(repository: _repo(client)),
        ),
      ));
      await tester.pumpAndSettle();
      expect(find.text("You haven't blocked anyone"), findsOneWidget);
    });

    testWidgets('lists blocked users with Unblock button', (tester) async {
      final client = _MockClient({
        'GET /blocks': () => _json(200, {
              'items': [
                {'blockedUserId': 'u2', 'createdAt': null},
              ],
              'total': 1,
            }),
      });
      await tester.pumpWidget(MaterialApp(
        home: BlockedUsersScreen(
          viewModel: BlockedUsersViewModel(repository: _repo(client)),
        ),
      ));
      await tester.pumpAndSettle();
      expect(find.text('u2'), findsOneWidget);
      expect(find.text('Unblock'), findsOneWidget);
    });
  });

  group('Report dialog', () {
    testWidgets('submits a report and shows confirmation', (tester) async {
      final client = _MockClient({
        'POST /reports': () => _json(201, {
              'reportId': 'r1',
              'targetType': 'submission',
              'targetId': 's1',
              'reason': 'spam',
              'status': 'open',
            }),
      });
      final repo = _repo(client);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (context) => TextButton(
              onPressed: () => showReportDialog(
                context,
                repository: repo,
                targetType: 'submission',
                targetId: 's1',
              ),
              child: const Text('open'),
            ),
          ),
        ),
      ));
      await tester.tap(find.text('open'));
      await tester.pumpAndSettle();

      expect(find.text('Report this submission'), findsOneWidget);
      await tester.tap(find.text('Spam or misleading'));
      await tester.pump();
      await tester.tap(find.widgetWithText(FilledButton, 'Report'));
      await tester.pumpAndSettle();

      expect(client.calls, contains('POST /reports'));
      expect(find.text('Report submitted. Thank you.'), findsOneWidget);
    });

    testWidgets('shows already-reported message on 409', (tester) async {
      final client = _MockClient({
        'POST /reports': () =>
            _json(409, {'detail': 'You have already reported this'}),
      });
      final repo = _repo(client);
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (context) => TextButton(
              onPressed: () => showReportDialog(
                context,
                repository: repo,
                targetType: 'user',
                targetId: 'u2',
                targetLabel: 'u2',
              ),
              child: const Text('open'),
            ),
          ),
        ),
      ));
      await tester.tap(find.text('open'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Harassment or bullying'));
      await tester.pump();
      await tester.tap(find.widgetWithText(FilledButton, 'Report'));
      await tester.pumpAndSettle();

      expect(find.text('You have already reported this.'), findsOneWidget);
    });
  });
}

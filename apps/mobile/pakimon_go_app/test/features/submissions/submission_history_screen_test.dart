import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/submissions/domain/submission_history_viewmodel.dart';
import 'package:pakimon_go_app/features/submissions/presentation/submission_history_screen.dart';

class _MockRepository extends CaptureRepository {
  _MockRepository() : super();

  @override
  Future<Map<String, dynamic>> getSubmissions({
    int limit = 20,
    int offset = 0,
    String? status,
    String sortBy = 'createdAt',
    String sortOrder = 'desc',
  }) {
    return Future.value({
      'submissions': <Map<String, dynamic>>[
        {
          'submissionId': 's1',
          'mediaAssetId': 'm1',
          'realName': 'Passer domesticus',
          'animalContext': 'wild',
          'scoreState': {
            'status': 'scored',
            'visiblePoints': 25,
            'explanationSummary': 'Wild species',
            'ledger': 'wild',
          },
          'visibility': 'private',
          'publicLocation': {
            'cellId': 'cell_abc123',
            'cellLatitude': 33.738,
            'cellLongitude': 73.084,
          },
        },
      ],
      'pagination': <String, dynamic>{'total': 1},
    });
  }
}

class _EmptyRepository extends CaptureRepository {
  _EmptyRepository() : super();

  @override
  Future<Map<String, dynamic>> getSubmissions({
    int limit = 20,
    int offset = 0,
    String? status,
    String sortBy = 'createdAt',
    String sortOrder = 'desc',
  }) {
    return Future.value({
      'submissions': <Map<String, dynamic>>[],
      'pagination': <String, dynamic>{'total': 0},
    });
  }
}

class _ErrorRepository extends CaptureRepository {
  _ErrorRepository() : super();

  @override
  Future<Map<String, dynamic>> getSubmissions({
    int limit = 20,
    int offset = 0,
    String? status,
    String sortBy = 'createdAt',
    String sortOrder = 'desc',
  }) {
    return Future.error('Network error');
  }
}

Widget _buildTestScreen(SubmissionHistoryViewModel vm) {
  return MaterialApp(
    home: Scaffold(
      body: SubmissionHistoryScreen(viewModel: vm),
    ),
  );
}

void main() {
  testWidgets('shows loading indicator initially',
      (WidgetTester tester) async {
    final repo = _MockRepository();
    final vm = SubmissionHistoryViewModel(repository: repo);

    await tester.pumpWidget(_buildTestScreen(vm));

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('shows submissions list after load',
      (WidgetTester tester) async {
    final repo = _MockRepository();
    final vm = SubmissionHistoryViewModel(repository: repo);

    await tester.pumpWidget(_buildTestScreen(vm));
    await tester.pumpAndSettle();

    expect(find.text('Passer domesticus'), findsOneWidget);
    expect(find.textContaining('25 pts'), findsOneWidget);
  });

  testWidgets('shows empty state when no submissions',
      (WidgetTester tester) async {
    final repo = _EmptyRepository();
    final vm = SubmissionHistoryViewModel(repository: repo);

    await tester.pumpWidget(_buildTestScreen(vm));
    await tester.pumpAndSettle();

    expect(find.text('No submissions yet'), findsOneWidget);
  });

  testWidgets('shows error state with retry button',
      (WidgetTester tester) async {
    final repo = _ErrorRepository();
    final vm = SubmissionHistoryViewModel(repository: repo);

    await tester.pumpWidget(_buildTestScreen(vm));
    await tester.pumpAndSettle();

    expect(find.text('Something went wrong'), findsOneWidget);
    expect(find.text('Retry'), findsOneWidget);
  });
}

import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/submissions/domain/submission_history_viewmodel.dart';

class _MockRepository extends CaptureRepository {
  _MockRepository() : super();

  final calls = <String>[];

  @override
  Future<Map<String, dynamic>> getSubmissions({
    int limit = 20,
    int offset = 0,
    String? status,
    String sortBy = 'createdAt',
    String sortOrder = 'desc',
  }) {
    calls.add('getSubmissions');
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

void main() {
  group('SubmissionHistoryViewModel', () {
    test('starts with empty state', () {
      final repo = _MockRepository();
      final vm = SubmissionHistoryViewModel(repository: repo);

      expect(vm.submissions, isEmpty);
      expect(vm.isLoading, false);
      expect(vm.error, isNull);
      expect(vm.total, 0);
    });

    test('fetchSubmissions populates list', () async {
      final repo = _MockRepository();
      final vm = SubmissionHistoryViewModel(repository: repo);

      await vm.fetchSubmissions();

      expect(vm.submissions.length, 1);
      expect(vm.submissions.first.realName, 'Passer domesticus');
      expect(vm.submissions.first.points, 25);
      expect(vm.isLoading, false);
      expect(vm.error, isNull);
      expect(vm.total, 1);
    });

  test('fetchSubmissions sets loading state', () async {
    final repo = _MockRepository();
    final vm = SubmissionHistoryViewModel(repository: repo);

    final states = <bool>[];
    vm.addListener(() => states.add(vm.isLoading));

    await vm.fetchSubmissions();

    expect(states, [true, false]);
  });

    test('fetchSubmissions handles errors', () async {
      final repo = _ErrorRepository();
      final vm = SubmissionHistoryViewModel(repository: repo);

      await vm.fetchSubmissions();

      expect(vm.submissions, isEmpty);
      expect(vm.error, isNotNull);
      expect(vm.total, 0);
      expect(vm.isLoading, false);
    });

    test('toMarker converts SubmissionResponse correctly', () async {
      final repo = _MockRepository();
      final vm = SubmissionHistoryViewModel(repository: repo);

      await vm.fetchSubmissions();

      final marker = vm.submissions.first.toMarker();
      expect(marker.submissionId, 's1');
      expect(marker.species, 'Passer domesticus');
      expect(marker.points, 25);
      expect(marker.status, 'scored');
      expect(marker.latitude, 33.738);
      expect(marker.longitude, 73.084);
    });
  });
}

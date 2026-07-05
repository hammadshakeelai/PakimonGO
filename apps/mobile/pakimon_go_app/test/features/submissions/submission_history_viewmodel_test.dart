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

/// Mirrors the REAL GET /v1/submissions list payload (submission_list.py),
/// which differs from the detail/create shape: `species`/`context`/`status`
/// plus a compact `scoreEvent` instead of `scoreState`/`publicLocation`.
class _ListShapeRepository extends CaptureRepository {
  _ListShapeRepository() : super();

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
          'submissionId': 'seed_sub_4',
          'userId': 'seed_user_alpha',
          'mediaAssetId': 'seed_media_4',
          'status': 'ai_evaluated',
          'submittedAt': '2026-07-03T17:32:22.414104',
          'createdAt': '2026-07-03T17:32:22.414255',
          'species': 'Golden Eagle',
          'context': 'wild',
          'cuteName': 'Golden Eagle',
          'caption': 'A beautiful Golden Eagle spotted in the wild!',
          'scoreEvent': {
            'points': 50,
            'ledger': 'wild',
            'explanation': 'wild',
          },
        },
      ],
      'pagination': <String, dynamic>{'limit': 20, 'offset': 0, 'total': 1},
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

    test('fetchSubmissions parses the real list-endpoint shape', () async {
      final repo = _ListShapeRepository();
      final vm = SubmissionHistoryViewModel(repository: repo);

      await vm.fetchSubmissions();

      expect(vm.error, isNull);
      expect(vm.submissions.length, 1);
      final sub = vm.submissions.first;
      expect(sub.realName, 'Golden Eagle');
      expect(sub.animalContext, 'wild');
      expect(sub.scoreState.status, 'ai_evaluated');
      expect(sub.points, 50);
      expect(sub.scoreState.ledger, 'wild');
      expect(sub.publicLocation, isEmpty);
      expect(vm.total, 1);
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

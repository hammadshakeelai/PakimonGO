import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/capture/domain/capture_media_service.dart';
import 'package:pakimon_go_app/features/capture/presentation/capture_screen.dart';
import 'package:pakimon_go_app/features/map/domain/map_viewmodel.dart';
import 'package:pakimon_go_app/features/map/presentation/map_screen.dart';
import 'package:pakimon_go_app/features/leaderboard/domain/leaderboard_viewmodel.dart';
import 'package:pakimon_go_app/features/leaderboard/presentation/leaderboard_screen.dart';
import 'package:pakimon_go_app/features/submissions/domain/submission_history_viewmodel.dart';
import 'package:pakimon_go_app/features/submissions/presentation/submission_history_screen.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class _NoOpMediaService implements CaptureMediaService {
  @override
  Future<CaptureMediaResult?> pickFromCamera() async => null;
  @override
  Future<CaptureMediaResult?> pickFromGallery() async => null;
}

class _NoOpRepository extends CaptureRepository {
  _NoOpRepository() : super();

  @override
  Future<List<SubmissionMarker>> getMapMarkers({int limit = 200}) {
    return Future.value([]);
  }

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

class _NoOpLeaderboardRepository extends CaptureRepository {
  _NoOpLeaderboardRepository() : super();

  @override
  Future<Map<String, dynamic>> getLeaderboard({
    int limit = 20,
    int offset = 0,
  }) {
    return Future.value({'entries': <dynamic>[], 'pagination': <String, dynamic>{'total': 0}});
  }
}

class _TestHomeScreen extends StatefulWidget {
  const _TestHomeScreen();

  @override
  State<_TestHomeScreen> createState() => _TestHomeScreenState();
}

class _TestHomeScreenState extends State<_TestHomeScreen> {
  int _currentIndex = 0;
  final _noOpRepo = _NoOpRepository();
  final _noOpLeaderboardRepo = _NoOpLeaderboardRepository();

  late final _screens = [
    MapScreen(viewModel: MapViewModel(repository: _noOpRepo)),
    CaptureScreen(mediaService: _NoOpMediaService()),
    SubmissionHistoryScreen(
        viewModel: SubmissionHistoryViewModel(repository: _noOpRepo)),
    LeaderboardScreen(
        viewModel: LeaderboardViewModel(repository: _noOpLeaderboardRepo)),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.map), label: 'Map'),
          NavigationDestination(
              icon: Icon(Icons.camera_alt), label: 'Capture'),
          NavigationDestination(
              icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(
              icon: Icon(Icons.leaderboard), label: 'Leaderboard'),
        ],
      ),
    );
  }
}

Widget _buildTestApp() {
  return MaterialApp(
    title: 'PakimonGO',
    home: const _TestHomeScreen(),
  );
}

void main() {
  testWidgets('app shows map screen as home', (WidgetTester tester) async {
    await tester.pumpWidget(_buildTestApp());
    await tester.pumpAndSettle();

    expect(find.text('PakimonGO Map'), findsOneWidget);
  });

  testWidgets('navigates to capture screen via bottom nav',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildTestApp());
    await tester.pumpAndSettle();

    await tester.tap(find.text('Capture'));
    await tester.pumpAndSettle();

    expect(find.text('Capture'), findsWidgets);
    expect(find.text('Camera'), findsOneWidget);
    expect(find.text('Gallery'), findsOneWidget);
  });
}

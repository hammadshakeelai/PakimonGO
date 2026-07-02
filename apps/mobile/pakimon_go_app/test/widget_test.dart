import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/domain/capture_media_service.dart';
import 'package:pakimon_go_app/features/capture/presentation/capture_screen.dart';
import 'package:pakimon_go_app/features/map/presentation/map_screen.dart';

class _NoOpMediaService implements CaptureMediaService {
  @override
  Future<CaptureMediaResult?> pickFromCamera() async => null;
  @override
  Future<CaptureMediaResult?> pickFromGallery() async => null;
}

class _TestHomeScreen extends StatefulWidget {
  const _TestHomeScreen();

  @override
  State<_TestHomeScreen> createState() => _TestHomeScreenState();
}

class _TestHomeScreenState extends State<_TestHomeScreen> {
  int _currentIndex = 0;

  final _screens = [
    const MapScreen(),
    CaptureScreen(mediaService: _NoOpMediaService()),
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

    expect(find.text('Test Capture'), findsOneWidget);
    expect(find.text('Camera'), findsOneWidget);
    expect(find.text('Gallery'), findsOneWidget);
  });
}

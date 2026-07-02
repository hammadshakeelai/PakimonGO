import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/map/presentation/marker_list_screen.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

Widget _buildScreen(List<SubmissionMarker> markers) {
  return MaterialApp(
    home: MarkerListScreen(markers: markers),
  );
}

void main() {
  final markers = [
    SubmissionMarker(
      submissionId: 's1',
      latitude: 51.5,
      longitude: -0.12,
      species: 'Passer domesticus',
      points: 25,
      status: 'scored',
    ),
    SubmissionMarker(
      submissionId: 's2',
      latitude: 48.85,
      longitude: 2.35,
      species: 'Felis catus',
      points: 1,
      status: 'capped',
    ),
  ];

  testWidgets('shows list of sightings with species names',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(markers));
    await tester.pumpAndSettle();

    expect(find.text('Sightings'), findsOneWidget);
    expect(find.text('Passer domesticus'), findsOneWidget);
    expect(find.text('Felis catus'), findsOneWidget);
  });

  testWidgets('shows status and coordinates in subtitle',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(markers));
    await tester.pumpAndSettle();

    expect(find.textContaining('scored'), findsOneWidget);
    expect(find.textContaining('capped'), findsOneWidget);
  });

  testWidgets('shows empty state when no markers',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen([]));
    await tester.pumpAndSettle();

    expect(find.text('No sightings yet'), findsOneWidget);
  });

  testWidgets('tapping a marker navigates to detail screen',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(markers));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Passer domesticus'));
    await tester.pumpAndSettle();

    expect(find.text('Photo preview'), findsOneWidget);
    expect(find.text('25'), findsOneWidget);
    expect(find.text('scored'), findsOneWidget);
  });
}

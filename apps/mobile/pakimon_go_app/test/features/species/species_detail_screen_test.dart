import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/species/presentation/species_detail_screen.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

Widget _buildScreen(SubmissionMarker marker) {
  return MaterialApp(
    home: SpeciesDetailScreen(marker: marker),
  );
}

void main() {
  final scoredMarker = SubmissionMarker(
    submissionId: 's1',
    mediaAssetId: 'm1',
    latitude: 51.5,
    longitude: -0.12,
    species: 'Passer domesticus',
    points: 25,
    status: 'scored',
  );

  final cappedMarker = SubmissionMarker(
    submissionId: 's2',
    mediaAssetId: 'm2',
    latitude: 48.85,
    longitude: 2.35,
    species: 'Felis catus',
    points: 1,
    status: 'capped',
  );

  testWidgets('shows species name in app bar', (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(scoredMarker));
    await tester.pumpAndSettle();

    expect(find.text('Passer domesticus'), findsAtLeastNWidgets(1));
  });

  testWidgets('shows photo with image network', (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(scoredMarker));
    await tester.pumpAndSettle();

    expect(find.byType(Image), findsOneWidget);
  });

  testWidgets('shows points, status, and coordinates', (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(scoredMarker));
    await tester.pumpAndSettle();

    expect(find.text('25'), findsOneWidget);
    expect(find.text('scored'), findsOneWidget);
    expect(find.text('51.5000'), findsOneWidget);
    expect(find.text('-0.1200'), findsOneWidget);
  });

  testWidgets('shows capped stats correctly', (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(cappedMarker));
    await tester.pumpAndSettle();

    expect(find.text('Felis catus'), findsAtLeastNWidgets(1));
    expect(find.text('capped'), findsOneWidget);
    expect(find.text('1'), findsOneWidget);
  });
}
